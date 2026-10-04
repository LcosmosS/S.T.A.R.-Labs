import pandas as pd


# Load dataset while ignoring invalid columns
df = pd.read_csv("your_file.csv", usecols=lambda column: column in valid_columns)


# Alternatively, use the `error_bad_lines` option to skip problematic rows
df = pd.read_csv("your_file.csv", error_bad_lines=False)


You can even selectively read columns by specifying valid column names (valid_columns), or use error_bad_lines=False to skip any problematic rows.
