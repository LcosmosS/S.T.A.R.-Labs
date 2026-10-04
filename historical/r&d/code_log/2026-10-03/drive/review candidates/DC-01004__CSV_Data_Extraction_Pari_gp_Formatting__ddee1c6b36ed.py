if missing_columns:
    print(f"Error: Missing columns: {missing_columns}")
    exit(1)


# Handle missing values with mean imputation
imputer = SimpleImputer(strategy='mean')
