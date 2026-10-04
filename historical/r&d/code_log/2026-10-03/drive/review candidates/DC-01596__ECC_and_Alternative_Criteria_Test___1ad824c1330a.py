    print("gudhi not installed. Run: pip install gudhi")
    gudhi = None


warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid')


# --- 3. Function Tracking ---
def log_function(func_name):
    print(f"Running {func_name}...")


# --- 4. Pre-Calculation NaN Handling ---
def impute_input_features(chunk, impute_cols=['ra', 'dec', 'z', 'metallicity'], target_cols=['logmass', 'petrorad_r']):
    log_function("impute_input_features")
    chunk = chunk.copy()
    imputer = KNNImputer(n_neighbors=5, weights='distance')
    X = chunk[impute_cols + target_cols]
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=impute_cols + target_cols, index=chunk.index)
    for target in target_cols:
        nan_idx = chunk[target].isna()
        if nan_idx.any():
            chunk.loc[nan_idx, target] = X_imputed.loc[nan_idx, target]
            print(f"impute_input_features: Imputed {target} for {nan_idx.sum()} rows")
    return chunk


# --- 5. Post-Calculation NaN Handling ---
def impute_derived_features(df, feature_cols):
    log_function("impute_derived_features")
    df = df.copy()
    imputer = KNNImputer(n_neighbors=5, weights='distance')
    X = df[feature_cols]
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=feature_cols, index=df.index)
    for col in feature_cols:
        nan_idx = df[col].isna()
        if nan_idx.any():
            df.loc[nan_idx, col] = X_imputed.loc[nan_idx, col]
            print(f"impute_derived_features: Imputed {col} for {nan_idx.sum()} rows")
    return df


# --- 6. Thermodynamic Entropy Calculation ---
def estimate_entropy(row):
    log_function("estimate_entropy")
    if not (np.isfinite(row['z']) and np.isfinite(row['metallicity']) and row['metallicity'] > 0):
        return np.nan
    T_proxy = row['z'] * 1e7  # Temperature (K) from redshift
    rho_proxy = row['metallicity'] * 1e-3  # Density (kg/m^3)
    try:
        S = KB * np.log(T_proxy / (rho_proxy ** (2/3)))
        return S
    except:
        return np.nan


# --- 7. Entropy Gradient Calculation ---
def compute_entropy_gradient(df, entropy_col='entropy', feature_cols=['logmass', 'petrorad_r']):
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
def compute_cohomology(df, coords_cols=['ra', 'dec', 'z'], entropy_col='entropy', max_dimension=1):
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
    simplex_tree.set_filtration(weights)  # Weight simplices by entropy
    persistence = simplex_tree.persistence()
    betti_numbers = simplex_tree.betti_numbers()
    betti_1 = betti_numbers[1] if len(betti_numbers) > 1 else 0
    df['betti_1'] = np.nan
    df.loc[X_coords.index, 'betti_1'] = betti_1
    print(f"compute_cohomology: Betti_1 = {betti_1}")
    return df, betti_1


# --- 9. KDE for Rank and L-Function ---
def compute_kde_features(df, rank_col='selmer_rank', lfunc_col='var_ap'):
    log_function("compute_kde_features")
    X_kde = df[[rank_col, lfunc_col]].dropna()
    if X_kde.empty:
        print("compute_kde_features: No valid data for KDE")
        return df, np.zeros(len(df))
    kde = KernelDensity(kernel='gaussian', bandwidth=0.5).fit(X_kde)
    log_dens = kde.score_samples(X_kde)
    df_kde = pd.DataFrame({f'kde_{rank_col}_{lfunc_col}': log_dens}, index=X_kde.index)
    df = df.join(df_kde)
    df[f'kde_{rank_col}_{lfunc_col}'] = df[f'kde_{rank_col}_{lfunc_col}'].fillna(0)
    print(f"compute_kde_features: Added KDE density for {rank_col} and {lfunc_col}")
    return df, log_dens


# --- 10. Scientific Derivation Functions ---
def calculate_distance_mpc(z):
    log_function("calculate_distance_mpc")
    if z is None or not np.isfinite(z) or z <= 0:
        return np.nan
    try:
        return float(cosmo.comoving_distance(z).to(u.Mpc).value)
    except:
        return np.nan


def convert_logmass_to_sm(logmass):
    log_function("convert_logmass_to_sm")
    if not np.isfinite(logmass):
        return np.nan
    return 10**logmass


def estimate_radius_ly(angular_size_arcsec, distance_mpc):
    log_function("estimate_radius_ly")
    if not (np.isfinite(angular_size_arcsec) and np.isfinite(distance_mpc) and
            angular_size_arcsec > 0 and distance_mpc > 0):
        return np.nan
    angle_rad = (angular_size_arcsec * u.arcsec).to(u.rad).value
    return angle_rad * distance_mpc * 3.262e6


# --- 11. Elliptic Curve Calculations ---
@parallel
def compute_3selmer_rank(delta, conductor, logmass, entropy, betti_1, entropy_gradient, pari):
    log_function("compute_3selmer_rank")
    if not all(np.isfinite(x) for x in [delta, conductor, logmass, entropy, betti_1, entropy_gradient]):
        print(f"compute_3selmer_rank: Skipped - Invalid delta={delta}, conductor={conductor}, logmass={logmass}, entropy={entropy}, betti_1={betti_1}, entropy_gradient={entropy_gradient}")
        return np.nan, 'invalid_input', np.nan, np.nan, np.nan
    try:
        scale_factor = max(1e3, delta / np.sqrt(MAX_CONDUCTOR))
        delta_scaled = int(delta / scale_factor)
        conductor_scaled = delta_scaled**2
        if conductor_scaled > MAX_CONDUCTOR:
            print(f"compute_3selmer_rank: Skipped - Scaled conductor={conductor_scaled} > MAX_CONDUCTOR")
            return np.nan, 'large_conductor', np.nan, np.nan, np.nan
        a = -delta_scaled
        b = delta_scaled**2 + entropy * logmass + COHOMOLOGY_WEIGHT * betti_1 + ENTROPY_GRADIENT_WEIGHT * entropy_gradient
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        rank = E.selmer_rank(3)
        torsion = E.torsion_subgroup().order()
        j_inv = E.j_invariant()
        disc = E.discriminant()
        print(f"compute_3selmer_rank: logmass={logmass:.3f}, delta_scaled={delta_scaled}, conductor_scaled={conductor_scaled}, entropy={entropy:.3e}, betti_1={betti_1}, entropy_gradient={entropy_gradient:.3e}, rank={rank}")
        if rank > SELMER_BOUND:
            print(f"compute_3selmer_rank: High rank={rank} > SELMER_BOUND={SELMER_BOUND}")
            return rank, 'high_rank', torsion, j_inv, disc
        return rank, 'success', torsion, j_inv, disc
    except Exception as e:
        print(f"compute_3selmer_rank: Error - {str(e)}")
        return np.nan, f'error_{str(e)}', np.nan, np.nan, np.nan


# --- 12. Mapping Functions ---
def compute_mappings(row, pari):
    log_function("compute_mappings")
    reg_cosmo = row['logmass'] * REG_COSMO * KAPPA if np.isfinite(row['logmass']) else np.nan
    t_cosmo = row['petrorad_r'] * T_COSMO * KAPPA if np.isfinite(row['petrorad_r']) else np.nan
    delta = row['logmass'] * 1e6 if np.isfinite(row['logmass']) else np.nan
    omega = row['petrorad_r'] * 1e3 if np.isfinite(row['petrorad_r']) else np.nan
    conductor = delta**2 if np.isfinite(delta) else np.nan
    j_invariant = row['metallicity'] * 1e4 if np.isfinite(row['metallicity']) else np.nan
    tr_p1 = float(factor(int(delta))[0][0]) if np.isfinite(delta) and delta > 0 else np.nan
    tr_p2 = float(factor(int(delta * 2))[0][0]) if np.isfinite(delta) and delta > 0 else np.nan
    tr_p3 = float(factor(int(delta * 3))[0][0]) if np.isfinite(delta) and delta > 0 else np.nan
    var_ap = np.var([tr_p1, tr_p2, tr_p3]) if all(np.isfinite([tr_p1, tr_p2, tr_p3])) else np.nan
    sato_tate = float(TARGET_PRIMES[0] * np.arccos(tr_p1 / (2 * np.sqrt(TARGET_PRIMES[0])))) if np.isfinite(tr_p1) and tr_p1 != 0 else np.nan
    isogeny_count = 1
    min_isogeny_deg = 1
    torsion_type = 1
    entropy = estimate_entropy(row)
    betti_1 = row.get('betti_1', np.nan)
    entropy_gradient = row.get('entropy_gradient', np.nan)
    selmer_rank, selmer_status, torsion, j_inv, disc = compute_3selmer_rank(delta, conductor, row['logmass'], entropy, betti_1, entropy_gradient, pari)
    return pd.Series({
        'reg_cosmo': reg_cosmo,
        't_cosmo': t_cosmo,
        'log_delta': np.log(abs(delta)) if np.isfinite(delta) and delta > 0 else np.nan,
        'log_omega': np.log(abs(omega)) if np.isfinite(omega) and omega > 0 else np.nan,
        'log_torsion': np.log(1 + torsion) if np.isfinite(torsion) else np.nan,
        'log_conductor': np.log(abs(conductor)) if np.isfinite(conductor) and conductor > 0 else np.nan,
        'real_log_j': np.log(abs(j_invariant)) if np.isfinite(j_invariant) and j_invariant != 0 else np.nan,
        'imag_log_j': 0.0,
        'tr_p1': tr_p1,
        'var_ap': var_ap,
        'sato_tate': sato_tate,
        'isogeny_count': isogeny_count,
        'log_min_isogeny': np.log(min_isogeny_deg) if min_isogeny_deg != 0 else np.nan,
        'log_torsion_type': np.log(1 + torsion_type),
        'selmer_rank': selmer_rank,
        'selmer_status': selmer_status,
        'torsion': torsion,
        'j_invariant': j_inv,
        'discriminant': disc,
        'entropy': entropy,
        'betti_1': betti_1,
        'entropy_gradient': entropy_gradient
    })


# --- 13. Generator Type Classification ---
def classify_generator(row):
    log_function("classify_generator")
    if pd.isna(row['log_delta']):
        return 'unknown', False
    is_simple = abs(row['log_delta'] - round(row['log_delta'])) < 0.1
    return 'Simple' if is_simple else 'Recursive', is_simple


# --- 14. Generator Structure Analysis ---
def analyze_generator_structure(coords):
    log_function("analyze_generator_structure")
    if pd.isna(coords):
        return {'type': 'unknown', 'structure': 'unknown'}
    x, y = coords if isinstance(coords, tuple) else (np.nan, np.nan)
    if pd.isna(x) or pd.isna(y):
        return {'type': 'unknown', 'structure': 'unknown'}
    if isinstance(x, (int, float)) and isinstance(y, (int, float)) and float(x).is_integer() and float(y).is_integer():
        return {'type': 'Simple', 'structure': 'integer'}
    denom_x = x.denominator() if hasattr(x, 'denominator') else 1
    denom_y = y.denominator() if hasattr(y, 'denominator') else 1
    factors_x = factor(denom_x) if denom_x != 1 else []
    if len(factors_x) == 1 and len(factors_x[0][0].prime_factors()) == 1:
        return {'type': 'Recursive', 'structure': 'power_of_prime'}
    return {'type': 'Recursive', 'structure': 'other_sequence'}


# --- 15. Preprocess Clustering Features ---
def preprocess_clustering_features(X_struct, feature_cols):
    log_function("preprocess_clustering_features")
    X_struct = X_struct.copy()
    imputer = KNNImputer(n_neighbors=5, weights='distance')
    X_struct[feature_cols] = imputer.fit_transform(X_struct[feature_cols])
    print(f"preprocess_clustering_features: Imputed NaN in {feature_cols}")
    return X_struct


# --- 16. Hyperparameter Optimization ---
def optimize_catboost_classifier(X, y, n_trials=50):
    log_function("optimize_catboost_classifier")
    if CatBoostClassifier is None or create_study is None:
        print("CatBoost or Optuna not installed. Skipping optimization.")
        return None
    def objective(trial):
        params = {
            'iterations': trial.suggest_int('iterations', 100, 1000),
            'depth': trial.suggest_int('depth', 4, 10),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
            'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1, 10)
        }
        model = CatBoostClassifier(**params, verbose=0)
        return cross_val_score(model, X, y, cv=5).mean()
    study = create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)
    return study.best_params


def optimize_catboost_regressor(X, y, n_trials=50):
    log_function("optimize_catboost_regressor")
    if CatBoostRegressor is None or create_study is None:
        print("CatBoost or Optuna not installed. Skipping optimization.")
        return None
    def objective(trial):
        params = {
            'iterations': trial.suggest_int('iterations', 100, 1000),
            'depth': trial.suggest_int('depth', 4, 10),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
            'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1, 10)
        }
        model = CatBoostRegressor(**params, verbose=0)
        return cross_val_score(model, X, y, cv=5, scoring='r2').mean()
    study = create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)
    return study.best_params


# --- 17. Symbolic Regression ---
def run_symbolic_regression(X, y, feature_cols, method='pysr'):
    log_function(f"run_symbolic_regression_{method}")
    if method == 'pysr' and PySRRegressor:
        model = PySRRegressor(
            niterations=40,
            binary_operators=["+", "-", "*", "/"],
            unary_operators=["log", "exp", "sqrt"],
            maxsize=20,
            model_selection="best"
        )
        model.fit(X[feature_cols], y)
        print(f"PySR Equations:\n", model.equations_)
        return model
    elif method == 'gplearn' and SymbolicRegressor:
        model = SymbolicRegressor(
            population_size=1000,
            generations=20,
            function_set=('add', 'sub', 'mul', 'div', 'log', 'sqrt'),
            metric='mse',
            random_state=42
        )
        model.fit(X[feature_cols], y)
        print(f"GPlearn Equation:\n", model._program)
        return model
    else:
        print(f"{method} not installed. Skipping symbolic regression.")
        return None


# --- 18. Interactive Visualization ---
def interactive_visualization(df, feature_cols):
    log_function("interactive_visualization")
    # Altair scatter plot with cohomology and entropy gradient
    chart = alt.Chart(df).mark_circle().encode(
        x=alt.X('selmer_rank:Q', title='3-Selmer Rank'),
        y=alt.Y('betti_1:Q', title='Betti Number (H1)'),
        color='generator_type:N',
        size='entropy_gradient:Q',
        tooltip=['objid', 'logmass', 'petrorad_r', 'selmer_rank', 'selmer_status', 'entropy', 'betti_1', 'entropy_gradient', 'kde_selmer_rank_var_ap']
    ).interactive().properties(
        width=800, height=400, title='Rank vs. Cohomology (Betti_1) by Generator Type and Entropy Gradient'
    )
    chart.save(f'{OUTPUT_PLOT_PREFIX}_interactive_scatter_cohomology.html')


    # Plotly 3D scatter plot
    fig = px.scatter_3d(
        df, x='logmass', y='entropy', z='betti_1',
        color='generator_type', size='entropy_gradient',
        hover_data=['objid', 'selmer_rank', 'selmer_status', 'entropy', 'betti_1', 'entropy_gradient', 'kde_selmer_rank_var_ap'],
        title='3D Galaxy Features with Cohomology and Entropy Gradient'
    )
    fig.write_html(f'{OUTPUT_PLOT_PREFIX}_3d_scatter_cohomology.html')


    # Persistence diagram
    if gudhi is not None:
        X_coords = df[['ra', 'dec', 'z', 'entropy']].dropna()
        if not X_coords.empty:
            rips_complex = gudhi.RipsComplex(points=X_coords[['ra', 'dec', 'z']], max_edge_length=1.0)
            simplex_tree = rips_complex.create_simplex_tree(max_dimension=2)
            simplex_tree.set_filtration(X_coords['entropy'].values)
            persistence = simplex_tree.persistence()
            gudhi.plot_persistence_diagram(persistence)
            plt.title('Persistence Diagram for Galaxy Coordinates (Entropy-Weighted)')
            plt.savefig(f'{OUTPUT_PLOT_PREFIX}_persistence_diagram.png')
            plt.close()


    # Entropy gradient vs. betti_1
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='entropy_gradient', y='betti_1', hue='generator_type', size='selmer_rank')
    plt.title('Entropy Gradient vs. Betti_1 by Generator Type')
    plt.savefig(f'{OUTPUT_PLOT_PREFIX}_entropy_gradient_betti1.png')
    plt.close()


    # t-SNE visualization
    X_valid = df[feature_cols].dropna()
    if not X_valid.empty:
        tsne = TSNE(n_components=2, random_state=42)
        X_tsne = tsne.fit_transform(X_valid)
        df_tsne = pd.DataFrame(X_tsne, columns=['TSNE1', 'TSNE2'], index=X_valid.index)
        df_tsne['generator_type'] = df.loc[X_valid.index, 'generator_type']
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df_tsne, x='TSNE1', y='TSNE2', hue='generator_type')
        plt.title('t-SNE of Galaxy Features with Cohomology and Entropy Gradient')
        plt.savefig(f'{OUTPUT_PLOT_PREFIX}_tsne_scatter_cohomology.png')
        plt.close()


    # Interactive widget
    @widgets.interact(feature=feature_cols)
    def plot_histogram(feature):
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x=feature, hue='generator_type', bins=50)
        plt.title(f'Distribution of {feature} by Generator Type')
        plt.savefig(f'{OUTPUT_PLOT_PREFIX}_histogram_{feature}.png')
        plt.show()


# --- 19. Shape Analysis ---
def analyze_noise_points(df, feature_cols):
    log_function("analyze_noise_points")
    recursive_df = df[df['generator_type'] == 'Recursive']
    noise_df = recursive_df[recursive_df['structure_cluster'] == -1]
    clustered_df = recursive_df[recursive_df['structure_cluster'] != -1]
    
    noise_stats = noise_df[feature_cols].describe()
    clustered_stats = clustered_df[feature_cols].describe()
    noise_nan_prop = noise_df[feature_cols].isna().mean()
    clustered_nan_prop = clustered_df[feature_cols].isna().mean()
    noise_structure_dist = noise_df['generator_structure'].apply(lambda x: x['structure'] if isinstance(x, dict) else 'unknown').value_counts()
    clustered_structure_dist = clustered_df['generator_structure'].apply(lambda x: x['structure'] if isinstance(x, dict) else 'unknown').value_counts()
    selmer_status_dist = df[df['generator_type'] == 'Recursive']['selmer_status'].value_counts()
    
    stats_df = pd.concat([noise_stats, clustered_stats], axis=1, keys=['Noise', 'Clustered'])
    stats_df.to_csv(f'{OUTPUT_PLOT_PREFIX}_noise_vs_clustered_stats.csv')
    noise_nan_prop.to_csv(f'{OUTPUT_PLOT_PREFIX}_noise_nan_proportion.csv')
    clustered_nan_prop.to_csv(f'{OUTPUT_PLOT_PREFIX}_clustered_nan_proportion.csv')
    noise_structure_dist.to_csv(f'{OUTPUT_PLOT_PREFIX}_noise_structure_distribution.csv')
    clustered_structure_dist.to_csv(f'{OUTPUT_PLOT_PREFIX}_clustered_structure_distribution.csv')
    selmer_status_dist.to_csv(f'{OUTPUT_PLOT_PREFIX}_selmer_status_distribution.csv')
    
    print("Noise Points Statistics:\n", noise_stats)
    print("\nClustered Points Statistics:\n", clustered_stats)
    print("\nNoise Points NaN Proportion:\n", noise_nan_prop)
    print("\nClustered Points NaN Proportion:\n", clustered_nan_prop)
    print("\nNoise Points Structure Distribution:\n", noise_structure_dist)
    print("\nClustered Points Structure Distribution:\n", clustered_structure_dist)
    print("\nSelmer Status Distribution:\n", selmer_status_dist)


# --- 20. Main Processing ---
def main():
    log_function("main")
    pari = Pari()
    chunks = pd.read_csv(INPUT_FILE, usecols=REQUIRED_COLUMNS, chunksize=CHUNKSIZE)
    df_list = []
    for i, chunk in enumerate(chunks):
        if ROW_LIMIT and i * CHUNKSIZE >= ROW_LIMIT:
            break
        log_function("process_chunk")
        chunk = impute_input_features(chunk)
        
        chunk['ra'] = chunk['ra'].where(chunk['ra'].notna(), -1)
        chunk['dec'] = chunk['dec'].where(chunk['dec'].notna(), -1)
        
        chunk['distance_mpc'] = chunk['z'].apply(calculate_distance_mpc)
        chunk['stellar_mass'] = chunk['logmass'].apply(convert_logmass_to_sm)
        chunk['radius_ly'] = chunk.apply(lambda x: estimate_radius_ly(x['petrorad_r'], x['distance_mpc']), axis=1)
        chunk[['reg_cosmo', 't_cosmo', 'log_delta', 'log_omega', 'log_torsion',
               'log_conductor', 'real_log_j', 'imag_log_j', 'tr_p1', 'var_ap',
               'sato_tate', 'isogeny_count', 'log_min_isogeny', 'log_torsion_type',
               'selmer_rank', 'selmer_status', 'torsion', 'j_invariant', 'discriminant', 'entropy', 'betti_1', 'entropy_gradient']] = chunk.apply(
                   lambda x: compute_mappings(x, pari), axis=1)
        
        chunk[['generator_type', 'is_simple_generator']] = chunk.apply(classify_generator, axis=1, result_type='expand')
        chunk['generator_coords'] = chunk['log_delta'].apply(lambda x: (x, x*2) if not pd.isna(x) else np.nan)
        chunk['generator_structure'] = chunk['generator_coords'].apply(analyze_generator_structure)
        
        df_list.append(chunk)


    df = pd.concat(df_list, ignore_index=True)


    # Compute cohomology
    df, betti_1 = compute_cohomology(df, entropy_col='entropy')


    # Compute entropy gradient
    df, entropy_gradient = compute_entropy_gradient(df)


    # Compute KDE features
    df, log_dens = compute_kde_features(df, 'selmer_rank', 'var_ap')


    # Check class distribution
    log_function("check_class_distribution")
    print("Generator Type Distribution:\n", df['generator_type'].value_counts())


    # NaN diagnostics
    log_function("nan_diagnostics")
    feature_cols = ['logmass', 'metallicity', 'petrorad_r', 'reg_cosmo', 't_cosmo', 'log_delta', 'log_omega',
                    'log_torsion', 'log_conductor', 'real_log_j', 'imag_log_j', 'tr_p1', 'var_ap', 'sato_tate',
                    'isogeny_count', 'log_min_isogeny', 'log_torsion_type', 'is_simple_generator', 'selmer_rank',
                    'torsion', 'j_invariant', 'discriminant', 'entropy', 'betti_1', 'entropy_gradient', 'kde_selmer_rank_var_ap']
    nan_counts = df[feature_cols].isna().sum()
    print("NaN Counts in Features:\n", nan_counts)
    nan_counts.to_csv(f'{OUTPUT_PLOT_PREFIX}_nan_counts.csv')


    # Impute derived features
    df = impute_derived_features(df, feature_cols)


    # Machine learning models for generator type
    X = df[feature_cols]
    y = df['generator_type']


    # Optimize CatBoost
    catboost_params_clf = optimize_catboost_classifier(X, y) if CatBoostClassifier and create_study else None
    classifiers = [
        ('RandomForest', RandomForestClassifier(random_state=42)),
        ('HistGradientBoosting', HistGradientBoostingClassifier(random_state=42))
