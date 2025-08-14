import unittest
import pandas as pd
import os
from sqlalchemy import create_engine, text
from assignment import prepare_data_for_ml

class TestDataPreparation(unittest.TestCase):
    def setUp(self):
        """Set up a temporary database and CSV file for testing"""
        self.engine = create_engine('sqlite:///:memory:')
        self.connection = self.engine.connect()
        self.csv_file_path = 'test_performance.csv'

        # Create and populate the employees table
        self.connection.execute(text("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT,
            start_date TEXT
        );
        """))
        self.connection.execute(text("""
        INSERT INTO employees (id, name, department, start_date) VALUES
        (1, 'Alice', 'IT', '2022-01-15'),
        (2, 'Bob', 'HR', '2021-11-20'),
        (3, 'Charlie', 'IT', '2023-03-10'),
        (4, 'David', 'Finance', '2020-05-01');
        """))
        self.connection.commit()

        # Create a dummy performance CSV file
        performance_data = {
            'employee_id': [1, 2, 4],
            'performance_score': [4.5, 3.8, 4.1]
        }
        pd.DataFrame(performance_data).to_csv(self.csv_file_path, index=False)

    def tearDown(self):
        """Clean up created files after each test"""
        self.connection.close()
        if os.path.exists(self.csv_file_path):
            os.remove(self.csv_file_path)
        if os.path.exists('prepared_data.csv'):
            os.remove('prepared_data.csv')

    def test_prepare_data_for_ml_creates_csv(self):
        """Test that the function creates the prepared_data.csv file"""
        prepare_data_for_ml(self.connection, self.csv_file_path)
        self.assertTrue(os.path.exists('prepared_data.csv'))

    def test_merged_data_shape_and_columns(self):
        """Test that the merged data has the correct shape and columns"""
        prepare_data_for_ml(self.connection, self.csv_file_path)
        df = pd.read_csv('prepared_data.csv')
        self.assertEqual(df.shape[0], 4)
        self.assertIn('days_since_start', df.columns)
        self.assertIn('dept_IT', df.columns)

    def test_missing_values_are_handled(self):
        """Test that missing performance scores are imputed correctly"""
        prepare_data_for_ml(self.connection, self.csv_file_path)
        df = pd.read_csv('prepared_data.csv')
        self.assertFalse(df['performance_score'].isnull().any())
        mean_score = (4.5 + 3.8 + 4.1) / 3
        self.assertAlmostEqual(df.loc[df['name'] == 'Charlie', 'performance_score'].iloc[0], mean_score, places=2)

    def test_feature_engineering_is_correct(self):
        """Test that the days_since_start feature is calculated correctly"""
        prepare_data_for_ml(self.connection, self.csv_file_path)
        df = pd.read_csv('prepared_data.csv')
        expected_days = (pd.to_datetime('2025-01-01') - pd.to_datetime('2022-01-15')).days
        self.assertEqual(df.loc[df['name'] == 'Alice', 'days_since_start'].iloc[0], expected_days)

    def test_one_hot_encoding_is_correct(self):
        """Test that one-hot encoding is applied correctly"""
        prepare_data_for_ml(self.connection, self.csv_file_path)
        df = pd.read_csv('prepared_data.csv')
        self.assertEqual(df.loc[df['name'] == 'Alice', 'dept_IT'].iloc[0], 1)
        self.assertEqual(df.loc[df['name'] == 'Alice', 'dept_HR'].iloc[0], 0)

if __name__ == '__main__':
    unittest.main()
