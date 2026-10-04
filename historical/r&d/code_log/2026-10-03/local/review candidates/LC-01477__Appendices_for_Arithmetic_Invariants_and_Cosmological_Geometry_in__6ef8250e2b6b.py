# Create a DataFrame for easier analysis
df = pd.DataFrame(analysis_results)

print("\n--- Stage 1 Complete: Foundational Dataset ---")
if not df.empty:
    df['x_coord'] = df['generator'].apply(lambda p: p[0])
    df['y_coord'] = df['generator'].apply(lambda p: p[1])
    df['x_num'] = df['x_coord'].apply(lambda x: x.numerator())
    df['x_den'] = df['x_coord'].apply(lambda x: x.denominator())
    df['y_num'] = df['y_coord'].apply(lambda y: y.numerator())
    df['y_den'] = df['y_coord'].apply(lambda y: y.denominator())
    print("Training Dataset:")
    print(df[['cluster', 'r', 'rho', 'generator']])
else:
    print("Training Dataset is empty.")

# --- ADDED VALIDATION BLOCK FROM PREVIOUS RESPONSE ---
if holdout_result is None:
    print(f"\n\033[91mCRITICAL PIPELINE ERROR:\033[0m")
    print(f"The designated holdout cluster, '{HOLDOUT_CLUSTER}', did not produce a
