        return np.nan
    T_proxy = row['z'] * 1e7  # Temperature (K) from redshift
    rho_proxy = row['metallicity'] * 1e-3  # Density (kg/m^3)
    try:
        S = KB * np.log(T_proxy / (rho_proxy ** (2/3)))
        return S
    except:
        return np.nan

# --- 7. Entropy Gradient Calculation ---
def compute_entropy_gradient(df, entropy_col='entropy', feature_cols=['logmass',
'petrorad_r']):
    log_function("compute_entropy_gradient")
    df = df.copy()
    X_valid = df[[entropy_col] + feature_cols].dropna()
    if X_valid.empty:
        print("compute_entropy_gradient: No valid data for gradient")
        return df, np.zeros(len(df))
    grad = np.zeros(len(df))
    for feat in feature_cols:
        grad_valid = np.gradient(X_valid[entropy_col], X_valid[feat])
        grad[X_valid.index] += grad_valid
    df['entropy_gradient'] = grad
    df['entropy_gradient'] = df['entropy_gradient'].fillna(0)
    print("compute_entropy_gradient: Computed entropy gradient")
    return df, grad

# --- 8. Cohomology Calculation ---
def compute_cohomology(df, coords_cols=['ra', 'dec', 'z'], entropy_col='entropy',
max_dimension=1):
    log_function("compute_cohomology")
    if gudhi is None:
        print("compute_cohomology: gudhi not installed. Returning NaN for betti_1")
        return df, np.full(len(df), np.nan)
    X_coords = df[coords_cols + [entropy_col]].dropna()
    if X_coords.empty:
        print("compute_cohomology: No valid coordinates for homology")
        return df, np.full(len(df), np.nan)
    points = X_coords[coords_cols].values
    weights = X_coords[entropy_col].values
    rips_complex = gudhi.RipsComplex(points=points, max_edge_length=1.0)
    simplex_tree = rips_complex.create_simplex_tree(max_dimension=max_dimension + 1)