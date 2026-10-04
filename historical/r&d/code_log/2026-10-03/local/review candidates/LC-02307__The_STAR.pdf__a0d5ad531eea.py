for col, fallback in required_cols.items():
    if col not in df.columns:
        if col == 'Av_gas_Re':
            if 'AV50' in df.columns and 'A0' in df.columns:
                df['Av_gas_Re'] = df['AV50'].fillna(df['A0']).fillna(0)
            elif 'AV50' in df.columns:
                df['Av_gas_Re'] = df['AV50'].fillna(0)
            elif 'A0' in df.columns:
                df['Av_gas_Re'] = df['A0'].fillna(0)
            else:
                df['Av_gas_Re'] = 0
            print("Assigned Av_gas_Re from AV50/A0")
        elif col == 'Age_LW_Re_fit':
            df['Age_LW_Re_fit'] = df.get('Age-Flame', 0)
            print("Assigned Age_LW_Re_fit from Age-Flame")
        elif col == 'ZH_LW_Re_fit':
            df['ZH_LW_Re_fit'] = df.get('met50', 0)
            print("Assigned ZH_LW_Re_fit from met50")
        elif col == 'cosmo_rank_L':
            df['cosmo_rank_L'] = df.get('cosmo_rank', 0.5)
            print("Assigned cosmo_rank_L from cosmo_rank")
        elif fallback:
            df[col] = df.get(fallback, np.nan)
            print(f"Warning: {col} not found. Using {fallback} as fallback.")
        else:
            print(f"Warning: {col} not found. Setting to 0.")
            df[col] = 0

# Feature engineering block with cosmic adjustments
========================================================================
===========================================
print(f"Memory usage before feature engineering: {df.memory_usage().sum() / 1024**2:.2f} MB")
