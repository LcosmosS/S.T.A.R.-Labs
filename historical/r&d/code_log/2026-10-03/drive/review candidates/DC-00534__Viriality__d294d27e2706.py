    return hiflugcs_sample


# Step 3: Compile Expanded Dataset (50+ unique)
def compile_expanded_dataset():
    initial_df = pd.DataFrame(initial_data)
    mcxc_df = pd.DataFrame(fetch_mcxc_data())
    hiflugcs_df = pd.DataFrame(fetch_hiflugcs_data())
    expanded_df = pd.concat([initial_df, mcxc_df, hiflugcs_df]).drop_duplicates(subset=['Name'])
    expanded_df.to_csv('expanded_dataset.csv', index=False)
    print(f"Compiled {len(expanded_df)} unique entries.")
    return expanded_df


# Step 4: Compute Virial Imbalance, a, b, Delta
K = 31.59  # Your calibration
def compute_parameters(row):
    M = row['Mvir_1e15Msun'] * 1e15  # M_sun
    sigma = row['sigma_kms'] * 1e3  # m/s
    R = row['Rvir_Mpc'] * 3.086e22  # m (1 Mpc = 3.086e22 m)
    # Virial Imbalance approximation: |2T + U| ≈ |3/2 M sigma^2 + G M^2 / R| (in M_sun (km/s)^2, scaled)
    T = (3/2) * M * (sigma / 1e3)**2  # Kinetic in M_sun (km/s)^2
    U = const.G.value * M**2 / R / (const.M_sun.value * (1e3)**2)  # Potential scaled
    energy = abs(2 * T + U)
    r = row['r_Mly']
    sigma, Rvir = row['sigma_kms'], row['Rvir_Mpc']
    a = round(-K * r)
    b = round((log10(M) * sigma / Rvir) * 2.0)
    delta = abs(-16 * (4 * a**3 + 27 * b**2))
    return pd.Series({'Energy': energy, 'a': a, 'b': b, 'Delta': delta})


# Step 5: Symbolic Regression with gplearn
def symbolic_regression(df):
    X = df['Delta'].values.reshape(-1, 1)
    y = df['Energy'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    est = SymbolicRegressor(population_size=5000, generations=20, verbose=1)
    est.fit(X_train, y_train)
    y_pred = est.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    print(f"Best Symbolic Model: {est._program}")
    print(f"R²: {r2}")
    return est


# Main Execution
if __name__ == "__main__":
    df = compile_expanded_dataset()
    df = df.join(df.apply(compute_parameters, axis=1))
    df.to_csv('computed_dataset.csv', index=False)
    model = symbolic_regression(df.dropna(subset=['Energy', 'Delta']))
