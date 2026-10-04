        else:
            df[col] = df[col].fillna(median_val)
            print(f"Imputed NaN in {col} with median {median_val}")


# Log NaN counts after imputation
for col in numeric_cols:
    nan_count = df[col].isna().sum()
    if nan_count > 0:
        print(f"NaN count in {col} after imputation: {nan_count}")
# Merge Diagnostics ===================================================================================================================================================
key_columns = ['objra_y', 'objdec', 'zsp', 'flux_Ha', 'logmass', 'petrorad_r']
