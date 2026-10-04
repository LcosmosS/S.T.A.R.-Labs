Q1 = df['SFR_PETRORAD_R'].quantile(0.25)
Q3 = df['SFR_PETRORAD_R'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 3 * IQR
upper_bound = Q3 + 3 * IQR
mask = (df['SFR_PETRORAD_R'] >= lower_bound) & (df['SFR_PETRORAD_R'] <= upper_bound)
df = df[mask]
print(f"Number of rows after IQR filtering: {len(df)}")
