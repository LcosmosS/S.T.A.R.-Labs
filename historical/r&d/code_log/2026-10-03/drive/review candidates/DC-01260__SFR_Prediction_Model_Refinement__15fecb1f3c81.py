# Check the SFR values to make sure there are no outliers or incorrect values
df1['SFR'] = df1['fS_x'] / (1.26e-41)  # SFR in solar masses per year


# Check for extreme values in SFR
print(df1['SFR'].describe())
df1 = df1[df1['SFR'] < 1e40]  # Filter out extreme SFR values
