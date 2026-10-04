if missing_columns:
    print(f"Error: Missing columns in the CSV file: {missing_columns}")
    exit(1)


# Handle missing values by imputing with the mean
imputer = SimpleImputer(strategy='mean')
