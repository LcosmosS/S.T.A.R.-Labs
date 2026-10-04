    df_clean['K_clipped'] = df_clean['scaling_constant_K'].clip(k_low, k_high)
    return df_clean

def run_exploratory_analysis(df):
    print("  - Generating Bayesian Binning plot on full dataset...")
