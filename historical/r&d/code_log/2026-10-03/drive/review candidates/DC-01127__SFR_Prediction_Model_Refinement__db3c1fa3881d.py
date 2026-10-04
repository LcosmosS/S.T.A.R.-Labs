def iqr_filter(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 3 * IQR
    upper = Q3 + 3 * IQR
    return df[(df[column] >= lower) & (df[column] <= upper)]


# Apply IQR filtering to relevant features (e.g., logmstar, mass_stellar_best_fit, SFR)
data_iqr_filtered = data_clean.copy()
columns_to_filter = ['logmstar', 'mass_stellar_best_fit', 'SFR_0_1Gyr_best_fit']


for col in columns_to_filter:
    data_iqr_filtered = iqr_filter(data_iqr_filtered, col)


print(f"Data size after IQR filtering: {data_iqr_filtered.shape[0]}")
