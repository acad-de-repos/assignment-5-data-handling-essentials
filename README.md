# Data Handling Essentials Assignment

## Problem Description

In this assignment, you will practice essential data handling techniques using a combination of Python's pandas library and SQL. You will work with a dataset that requires cleaning, transformation, and feature engineering to prepare it for machine learning applications. This assignment covers fundamental data wrangling skills that are crucial for any data-related role.

## Learning Objectives

By completing this assignment, you will learn:
- How to load data from a CSV file and a database
- How to handle missing values and incorrect data types
- How to merge data from different sources
- How to create new features using a combination of columns
- How to export cleaned data to a new CSV file

## Setup Instructions

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure you have the following packages installed:
   - pandas (>=1.3.0)
   - sqlalchemy (>=1.4.0)
   - scikit-learn (>=1.0.0)

## Instructions

1. Open the `assignment.py` file.
2. You will find a function definition: `prepare_data_for_ml(db_connection, csv_file_path)`.
3. The function takes a database connection and a CSV file path as input.
4. Your tasks are to:
   *   **Task 1**: Load the `employees` data from the database and the `employee_performance` data from the CSV file.
   *   **Task 2**: Merge the two datasets based on the employee ID.
   *   **Task 3**: Clean the merged dataset by handling missing values in the `performance_score` column (impute with the mean) and converting the `start_date` to a datetime object.
   *   **Task 4**: Create a new feature called `days_since_start` which calculates the number of days from the `start_date` to a reference date (e.g., '2025-01-01').
   *   **Task 5**: One-hot encode the `department` column to prepare it for machine learning models.
   *   **Task 6**: Export the final prepared dataset to a new CSV file named `prepared_data.csv`.

## Hints

*   Use `pd.read_sql_table()` and `pd.read_csv()` to load the data.
*   Use `pd.merge()` to combine the two DataFrames.
*   Use `.fillna()` to handle missing values and `pd.to_datetime()` to convert the date column.
*   Subtracting two datetime objects results in a timedelta object; use `.dt.days` to get the number of days.
*   Use `pd.get_dummies()` for one-hot encoding.
*   Use `df.to_csv()` to export the final DataFrame.

## Testing Your Solution

Run the test file to verify your implementation:
```bash
python test.py
```

The tests will check:
- That the function creates the `prepared_data.csv` file
- That the merged dataset has the correct shape and columns
- That missing values are handled correctly
- That the new features are calculated accurately
- That the one-hot encoding is applied correctly

## Expected Output

Your function should create a new CSV file named `prepared_data.csv` containing the fully cleaned and prepared dataset, ready for use in a machine learning model.

## Sample Data Format

### `employees` table (in the database):
- `id` (INTEGER, PRIMARY KEY)
- `name` (TEXT)
- `department` (TEXT)
- `start_date` (TEXT)

### `employee_performance` data (in the CSV file):
- `employee_id` (INTEGER)
- `performance_score` (FLOAT)

## Troubleshooting

### Common Errors
- `MergeError`: Ensure the columns you are merging on have the same name and data type.
- `ValueError`: Check for incorrect data formats, especially in the `start_date` column.
- `FileNotFoundError`: Make sure the CSV file path is correct.

## Further Exploration (Optional)

*   Explore other imputation techniques for missing values (e.g., median, mode).
*   Try other feature engineering techniques, such as creating interaction terms or polynomial features.
*   How would you handle categorical features with a large number of unique values?
*   Look into using scikit-learn's `ColumnTransformer` for more complex data preprocessing pipelines.

## Resources

- [Pandas Merging 101](https://pandas.pydata.org/docs/user_guide/merging.html)
- [Handling Missing Data in Pandas](https://pandas.pydata.org/docs/user_guide/missing_data.html)
- [Pandas `get_dummies` Documentation](https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html)
- [Feature Engineering with Python](https://towardsdatascience.com/feature-engineering-for-machine-learning-3a5e293a5114)
