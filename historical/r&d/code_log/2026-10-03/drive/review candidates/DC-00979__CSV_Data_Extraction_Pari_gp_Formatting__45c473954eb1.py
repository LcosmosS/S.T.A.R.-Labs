# Replace invalid values (-9999) with NaN
df.replace(-9999, np.nan, inplace=True)


# Check for required columns
required_columns = ['logmass', 'z', 'morphology']
if not all(col in df.columns for col in required_columns):
    print("Error: Missing required columns. Adjust the script to use available columns.")
    exit(1)


# Impute missing values with mean
imputer = SimpleImputer(strategy='mean')
