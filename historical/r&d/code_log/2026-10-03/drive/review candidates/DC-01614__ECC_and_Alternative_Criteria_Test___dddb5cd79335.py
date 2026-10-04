    print("gudhi not installed. Run: pip install gudhi") 
    gudhi = None 
from scipy.spatial.distance import cdist
import multiprocessing as mp
import gc


warnings.filterwarnings('ignore') 
plt.style.use('seaborn-v0_8-whitegrid') 


# Logging to files
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)
analysis_logger = logging.getLogger('analysis')
analysis_handler = logging.FileHandler('analysis.log')
analysis_logger.addHandler(analysis_handler)
analysis_logger.setLevel(logging.INFO)


# --- 3. Print Step Function ---
def print_step(step_num, step_name, summary=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[STEP {step_num}] {timestamp} - {step_name}")
    logging.info(f"Step {step_num}: {step_name}")
    if summary is not None:
        print(f"[SUMMARY {step_num}] {step_name} completed.")
        for key, value in summary.items():
            print(f"  {key}: {value}")
        analysis_logger.info(f"Step {step_num} Summary: {summary}")


# --- 4. Pre-Calculation NaN Handling --- 
def impute_input_features(chunk, impute_cols=['ra', 'dec', 'z', 'metallicity'], target_cols=['logmass', 'petrorad_r']): 
    chunk = chunk.copy() 
    imputer = KNNImputer(n_neighbors=5, weights='distance') 
    X = chunk[impute_cols + target_cols] 
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=impute_cols + target_cols, index=chunk.index) 
    for target in target_cols: 
        nan_idx = chunk[target].isna() 
        if nan_idx.any(): 
            chunk.loc[nan_idx, target] = X_imputed.loc[nan_idx, target] 
            logging.debug(f"impute_input_features: Imputed {target} for {nan_idx.sum()} rows") 
    chunk['z'] = np.clip(chunk['z'], 1e-6, None)
    chunk['metallicity'] = np.clip(np.abs(chunk['metallicity']) + 1e-6, 1e-6, None)
    summary = {
        'Imputed logmass': np.int64(chunk['logmass'].isna().sum()),
        'Imputed petrorad_r': np.int64(chunk['petrorad_r'].isna().sum()),
        'z_min': chunk['z'].min(),
        'metallicity_min': chunk['metallicity'].min()
    }
    logging.debug(f"impute_input_features: {summary}")
    return chunk, summary


# --- 5. Post-Calculation NaN Handling --- 
def impute_derived_features(df, feature_cols): 
    df = df.copy() 
    imputer = KNNImputer(n_neighbors=5, weights='distance') 
    available_cols = [col for col in feature_cols if col in df.columns]
    X = df[available_cols] 
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=available_cols, index=df.index) 
    for col in available_cols: 
        nan_idx = df[col].isna() 
        if nan_idx.any(): 
            df.loc[nan_idx, col] = X_imputed.loc[nan_idx, col] 
            logging.debug(f"impute_derived_features: Imputed {col} for {nan_idx.sum()} rows") 
    return df 


# --- 6. Thermodynamic Entropy Calculation --- 
def estimate_entropy(row, median_entropy=0): 
    from astropy.cosmology.units import redshift_temperature
    try:
        T_proxy = redshift_temperature(cosmo.Tcmb(0) * (1 + row['z'])).value 
        rho_proxy = max(1e-6, abs(row['metallicity']) * 1e-3)
        S = KB * np.log(T_proxy / (rho_proxy ** (2/3)))
        summary = {'Entropy': S, 'Status': 'Computed'}
        if not np.isfinite(S):
            summary = {'Entropy': median_entropy, 'Status': 'Fallback to median'}
        return S if np.isfinite(S) else median_entropy, summary
    except Exception as e:
        logging.debug(f"estimate_entropy: Error - {str(e)}")
        return median_entropy, {'Entropy': median_entropy, 'Status': f'Error: {str(e)}'}


# --- 7. Entropy Gradient Calculation --- 
def compute_entropy_gradient(df, entropy_col='entropy', feature_cols=['logmass', 'petrorad_r']): 
    df = df.copy() 
    X_valid = df[[entropy_col] + feature_cols].dropna() 
    summary = {'Valid Rows': len(X_valid)}
    if X_valid.empty: 
        logging.warning("compute_entropy_gradient: No valid data for gradient") 
        return df, np.zeros(len(df)), summary
    grad = np.zeros(len(df)) 
    for feat in feature_cols: 
        grad_valid = np.gradient(X_valid[entropy_col], X_valid[feat]) 
        grad[X_valid.index] += grad_valid 
    df['entropy_gradient'] = grad 
    df['entropy_gradient'] = df['entropy_gradient'].fillna(0) 
    summary['Gradient Mean'] = np.mean(grad) if np.isfinite(grad).any() else np.nan
    analysis_logger.info("compute_entropy_gradient: Computed entropy gradient")
    return df, grad, summary


# --- 8. Cohomology Calculation --- 
def compute_cohomology(df, coords_cols=['ra', 'dec', 'z'], entropy_col='entropy', max_dimension=2): 
    if gudhi is None: 
        logging.warning("compute_cohomology: gudhi not installed. Returning NaN for betti_1") 
        summary = {'Status': 'gudhi not installed', 'Betti_1': 'NaN'}
        return df, np.full(len(df), np.nan), summary
    X_coords = df[coords_cols + [entropy_col]].dropna() 
    summary = {'Valid Rows': len(X_coords)}
    if X_coords.empty: 
        logging.warning("compute_cohomology: No valid coordinates for homology") 
        summary['Status'] = 'No valid coordinates'
        return df, np.full(len(df), np.nan), summary
    if len(X_coords) > MAX_COHOM_POINTS:
        X_coords = X_coords.sample(MAX_COHOM_POINTS, random_state=42)
        summary['Subsampled Rows'] = MAX_COHOM_POINTS
        logging.info(f"Subsampled to {MAX_COHOM_POINTS} points for cohomology")
    points = X_coords[coords_cols].values 
    # Scale coordinates to improve distance calculations
    scaler = StandardScaler()
    points = scaler.fit_transform(points)
    weights = X_coords[entropy_col].values 
    weights = np.where(np.isfinite(weights), weights, np.median(weights[np.isfinite(weights)]))  # Handle NaN weights
    dist = cdist(points, points) 
    w_rips = WeightedRipsComplex(distance_matrix=dist, weights=weights) 
    simplex_tree = w_rips.create_simplex_tree(max_dimension=max_dimension + 1) 
    persistence = simplex_tree.persistence() 
    betti_numbers = simplex_tree.betti_numbers() 
    betti_1 = betti_numbers[1] if len(betti_numbers) > 1 else 0 
    df['betti_1'] = np.nan 
    df.loc[X_coords.index, 'betti_1'] = betti_1 
    summary['Betti_1'] = betti_1
    analysis_logger.info(f"compute_cohomology: Betti_1 = {betti_1}")
    return df, betti_1, summary


# --- 9. KDE for Rank and L-Function --- 
def compute_kde_features(df, rank_col='selmer_rank', lfunc_col='var_ap'): 
    X_kde = df[[rank_col, lfunc_col]].dropna() 
    summary = {'Valid Rows': len(X_kde)}
    if X_kde.empty: 
        logging.warning("compute_kde_features: No valid data for KDE") 
        summary['Status'] = 'No valid data'
        return df, np.zeros(len(df)), summary
    kde = KernelDensity(kernel='gaussian', bandwidth=0.5).fit(X_kde) 
    log_dens = kde.score_samples(X_kde) 
    df_kde = pd.DataFrame({f'kde_{rank_col}_{lfunc_col}': log_dens}, index=X_kde.index) 
    df = df.join(df_kde) 
    df[f'kde_{rank_col}_{lfunc_col}'] = df[f'kde_{rank_col}_{lfunc_col}'].fillna(0) 
    summary['KDE Density Mean'] = np.mean(log_dens) if np.isfinite(log_dens).any() else np.nan
    analysis_logger.info(f"compute_kde_features: Added KDE density for {rank_col} and {lfunc_col}")
    return df, log_dens, summary


# --- 10. Scientific Derivation Functions --- 
def calculate_distance_mpc(z): 
    if z is None or not np.isfinite(z) or z <= 0: 
        return np.nan, {'Distance': np.nan, 'Status': 'Invalid input'}
    try: 
        distance = float(cosmo.comoving_distance(z).to(u.Mpc).value) 
        return distance, {'Distance': distance, 'Status': 'Computed'}
    except Exception as e: 
        logging.debug(f"calculate_distance_mpc: Error - {str(e)}")
        return np.nan, {'Distance': np.nan, 'Status': f'Error: {str(e)}'}


def convert_logmass_to_sm(logmass): 
    if not np.isfinite(logmass): 
        return np.nan 
    return 10**logmass 


def estimate_radius_ly(angular_size_arcsec, distance_mpc): 
    if not (np.isfinite(angular_size_arcsec) and np.isfinite(distance_mpc) and angular_size_arcsec > 0 and distance_mpc > 0): 
        return np.nan 
    angle_rad = (angular_size_arcsec * u.arcsec).to(u.rad).value 
    return angle_rad * distance_mpc * 3.262e6 


# --- 11. Elliptic Curve Calculations --- 
@parallel(ncpus=4)
def compute_3selmer_rank(delta, conductor, logmass, entropy, betti_1, entropy_gradient, pari): 
    entropy = 0 if np.isnan(entropy) else entropy
    betti_1 = 0 if np.isnan(betti_1) else betti_1
    entropy_gradient = 0 if np.isnan(entropy_gradient) else entropy_gradient
    if not all(np.isfinite(x) for x in [delta, conductor, logmass]): 
        logging.debug(f"compute_3selmer_rank: Skipped - Invalid delta={delta}, conductor={conductor}, logmass={logmass}") 
        return np.nan, 'invalid_input', np.nan, np.nan, np.nan, {'Rank': 'NaN', 'Status': 'invalid_input'}
    try: 
        scale_factor = max(1e3, np.log10(max(1, abs(delta)))) 
        delta_scaled = int(delta / scale_factor) 
        conductor_scaled = min(int(delta_scaled**2), MAX_CONDUCTOR) 
        if conductor_scaled > MAX_CONDUCTOR: 
            logging.debug(f"compute_3selmer_rank: Skipped - Scaled conductor={conductor_scaled} > MAX_CONDUCTOR") 
            return np.nan, 'large_conductor', np.nan, np.nan, np.nan, {'Rank': 'NaN', 'Status': 'large_conductor'}
        a = -delta_scaled 
        b = delta_scaled**2 + entropy * logmass + COHOMOLOGY_WEIGHT * betti_1 + ENTROPY_GRADIENT_WEIGHT * entropy_gradient 
        E = EllipticCurve(QQ, [0, 0, 0, a, b]).minimal_model() 
        try:
            rank = E.rank()  # Fallback to rank() instead of selmer_rank(3)
        except Exception as e:
            logging.error(f"compute_3selmer_rank: Rank computation failed - {str(e)}")
            return np.nan, f'error_{str(e)}', np.nan, np.nan, np.nan, {'Rank': 'NaN', 'Status': f'error_{str(e)}'}
        torsion = E.torsion_subgroup().order() 
        j_inv = E.j_invariant() 
        disc = E.discriminant() 
        summary = {
            'Rank': rank,
            'Status': 'success' if rank <= SELMER_BOUND else 'high_rank',
            'Logmass': logmass,
            'Delta_Scaled': delta_scaled,
            'Conductor_Scaled': conductor_scaled,
            'Entropy': entropy,
            'Betti_1': betti_1,
            'Entropy_Gradient': entropy_gradient
        }
        analysis_logger.info(f"compute_3selmer_rank: {summary}")
        if rank > SELMER_BOUND: 
            logging.debug(f"compute_3selmer_rank: High rank={rank} > SELMER_BOUND={SELMER_BOUND}")
        return rank, 'success' if rank <= SELMER_BOUND else 'high_rank', torsion, j_inv, disc, summary
    except Exception as e: 
        logging.error(f"compute_3selmer_rank: Error - {str(e)}") 
        return np.nan, f'error_{str(e)}', np.nan, np.nan, np.nan, {'Rank': 'NaN', 'Status': f'error_{str(e)}'}


# --- 12. Mapping Functions --- 
def compute_mappings(row, pari): 
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
    entropy, entropy_summary = estimate_entropy(row) 
    betti_1 = row.get('betti_1', np.nan) 
    entropy_gradient = row.get('entropy_gradient', np.nan) 
    selmer_rank, selmer_status, torsion, j_inv, disc, selmer_summary = compute_3selmer_rank(delta, conductor, row['logmass'], entropy, betti_1, entropy_gradient, pari) 
    summary = {
        'Reg_Cosmo': reg_cosmo,
        'T_Cosmo': t_cosmo,
        'Log_Delta': np.log(abs(delta)) if np.isfinite(delta) and delta > 0 else np.nan,
        'Selmer_Rank': selmer_rank,
        'Selmer_Status': selmer_status
    }
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
    }), summary


# --- 13. Generator Type Classification --- 
def classify_generator(row): 
    if pd.isna(row['log_delta']): 
        return 'unknown', False, {'Generator_Type': 'unknown', 'Is_Simple': False}
    is_simple = abs(row['log_delta'] - round(row['log_delta'])) < 0.1 
    generator_type = 'Simple' if is_simple else 'Recursive'
    return generator_type, is_simple, {'Generator_Type': generator_type, 'Is_Simple': is_simple}


# --- 14. Generator Structure Analysis --- 
def analyze_generator_structure(coords): 
    if pd.isna(coords): 
        return {'type': 'unknown', 'structure': 'unknown'}, {'Type': 'unknown', 'Structure': 'unknown'}
    x, y = coords if isinstance(coords, tuple) else (np.nan, np.nan) 
    if pd.isna(x) or pd.isna(y): 
        return {'type': 'unknown', 'structure': 'unknown'}, {'Type': 'unknown', 'Structure': 'unknown'}
    if isinstance(x, (int, float)) and isinstance(y, (int, float)) and float(x).is_integer() and float(y).is_integer(): 
        return {'type': 'Simple', 'structure': 'integer'}, {'Type': 'Simple', 'Structure': 'integer'}
    denom_x = x.denominator() if hasattr(x, 'denominator') else 1 
    denom_y = y.denominator() if hasattr(y, 'denominator') else 1 
    factors_x = factor(denom_x) if denom_x != 1 else [] 
    if len(factors_x) == 1 and len(factors_x[0][0].prime_factors()) == 1: 
        return {'type': 'Recursive', 'structure': 'power_of_prime'}, {'Type': 'Recursive', 'Structure': 'power_of_prime'}
    return {'type': 'Recursive', 'structure': 'other_sequence'}, {'Type': 'Recursive', 'Structure': 'other_sequence'}


# --- 15. Preprocess Clustering Features --- 
def preprocess_clustering_features(X_struct, feature_cols): 
    X_struct = X_struct.copy() 
    imputer = KNNImputer(n_neighbors=5, weights='distance') 
    available_cols = [col for col in feature_cols if col in X_struct.columns]
    X_struct[available_cols] = imputer.fit_transform(X_struct[available_cols]) 
    analysis_logger.info(f"preprocess_clustering_features: Imputed NaN in {available_cols}")
    return X_struct 


# --- 16. Hyperparameter Optimization --- 
def optimize_catboost_classifier(X, y, n_trials=50): 
    if CatBoostClassifier is None or create_study is None: 
        logging.warning("CatBoost or Optuna not installed. Skipping optimization.") 
        return None 
    def objective(trial): 
        params = { 
            'iterations': trial.suggest_int('iterations', 100, 1000), 
            'depth': trial.suggest_int('depth', 4, 10), 
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True), 
            'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1, 10) 
        } 
        model = CatBoostClassifier(**params, verbose=0) 
        return cross_val_score(model, X, y, cv=5, n_jobs=-1).mean() 
    study = create_study(direction='maximize') 
    study.optimize(objective, n_trials=n_trials, n_jobs=-1) 
    return study.best_params 


def optimize_catboost_regressor(X, y, n_trials=50): 
    if CatBoostRegressor is None or create_study is None: 
        logging.warning("CatBoost or Optuna not installed. Skipping optimization.") 
        return None 
    def objective(trial): 
        params = { 
            'iterations': trial.suggest_int('iterations', 100, 1000), 
            'depth': trial.suggest_int('depth', 4, 10), 
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True), 
            'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1, 10) 
        } 
        model = CatBoostRegressor(**params, verbose=0) 
        return cross_val_score(model, X, y, cv=5, scoring='r2', n_jobs=-1).mean() 
    study = create_study(direction='maximize') 
    study.optimize(objective, n_trials=n_trials, n_jobs=-1) 
    return study.best_params 


# --- 17. Symbolic Regression --- 
def run_symbolic_regression(X, y, feature_cols, method='pysr'): 
    available_cols = [col for col in feature_cols if col in X.columns]
    if method == 'pysr' and PySRRegressor: 
        model = PySRRegressor( 
            niterations=40, 
            binary_operators=["+", "-", "*", "/"], 
            unary_operators=["log", "exp", "sqrt"], 
            maxsize=20, 
            model_selection="best" 
        ) 
        model.fit(X[available_cols], y) 
        analysis_logger.info(f"PySR Equations:\n {model.equations_}")
        return model 
    elif method == 'gplearn' and SymbolicRegressor: 
        model = SymbolicRegressor( 
            population_size=1000, 
            generations=20, 
            function_set=('add', 'sub', 'mul', 'div', 'log', 'sqrt'), 
            metric='mse', 
            random_state=42 
        ) 
        model.fit(X[available_cols], y) 
        analysis_logger.info(f"GPlearn Equation:\n {model._program}")
        return model 
    else: 
        logging.warning(f"{method} not installed. Skipping symbolic regression.") 
        return None 


# --- 18.1. 3D Manifold Visualization ---
def visualize_3d_manifold(df, coords_cols=['ra', 'dec', 'z'], weight_col='entropy', color_col='generator_type'):
    if gudhi is None:
        logging.warning("visualize_3d_manifold: gudhi not installed. Skipping manifold video.")
        return {'Status': 'gudhi not installed'}
    
    X_coords = df[coords_cols + [weight_col, color_col]].dropna()
    summary = {'Valid Rows': len(X_coords)}
    if X_coords.empty:
        logging.warning("visualize_3d_manifold: No valid coordinates for manifold visualization")
        summary['Status'] = 'No valid coordinates'
        return summary
    
    if len(X_coords) > MAX_COHOM_POINTS:
        X_coords = X_coords.sample(MAX_COHOM_POINTS, random_state=42)
        summary['Subsampled Rows'] = MAX_COHOM_POINTS
        logging.info(f"Subsampled to {MAX_COHOM_POINTS} points for manifold visualization")
    
    points = X_coords[coords_cols].values
    scaler = StandardScaler()
    points = scaler.fit_transform(points)  # Scale coordinates
    weights = X_coords[weight_col].values
    weights = np.where(np.isfinite(weights), weights, np.median(weights[np.isfinite(weights)]))  # Handle NaN weights
    colors = X_coords[color_col].map({'Simple': 'blue', 'Recursive': 'red', 'unknown': 'gray'})
    
    # Compute Weighted Rips Complex
    dist = cdist(points, points)
    w_rips = WeightedRipsComplex(distance_matrix=dist, weights=weights)
    simplex_tree = w_rips.create_simplex_tree(max_dimension=2)
    
    # Collect simplices (vertices, edges, triangles)
    simplices = []
    for simplex, _ in simplex_tree.get_simplices():
        simplices.append(simplex)
    
    # Initialize plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    def update_frame(i):
        ax.clear()
        ax.set_xlabel('RA (scaled)')
        ax.set_ylabel('Dec (scaled)')
        ax.set_zlabel('z (scaled)')
        ax.set_title(f'3D Manifold Construction (Simplex {i+1}/{len(simplices)})')
        
        # Plot simplices up to frame i
        for j in range(min(i + 1, len(simplices))):
            simplex = simplices[j]
            if len(simplex) == 1:  # Vertex
                idx = simplex[0]
                ax.scatter(points[idx, 0], points[idx, 1], points[idx, 2], c=colors.iloc[idx], s=50, alpha=0.6)
            elif len(simplex) == 2:  # Edge
                idx1, idx2 = simplex
                x = [points[idx1, 0], points[idx2, 0]]
                y = [points[idx1, 1], points[idx2, 1]]
                z = [points[idx1, 2], points[idx2, 2]]
                ax.plot(x, y, z, c='black', alpha=0.3)
            elif len(simplex) == 3:  # Triangle
                idx1, idx2, idx3 = simplex
                x = [points[idx1, 0], points[idx2, 0], points[idx3, 0], points[idx1, 0]]
                y = [points[idx1, 1], points[idx2, 1], points[idx3, 1], points[idx1, 1]]
                z = [points[idx1, 2], points[idx2, 2], points[idx3, 2], points[idx1, 2]]
                ax.plot(x, y, z, c='blue', alpha=0.2)
        
        # Adjust view
        ax.view_init(elev=20, azim=i * 2)  # Rotate view for dynamic effect
    
    # Create animation
    anim = animation.FuncAnimation(fig, update_frame, frames=len(simplices), interval=100)
    output_file = f'{OUTPUT_PLOT_PREFIX}_3d_manifold.mp4'
    anim.save(output_file, writer='ffmpeg', fps=30)
    plt.close()
    
    summary['Manifold Video'] = output_file
    analysis_logger.info(f"visualize_3d_manifold: Saved manifold video to {output_file}")
    return summary


# --- 18.2. Interactive Visualization --- 
def interactive_visualization(df, feature_cols): 
    print_step(18, "Interactive Visualization")
    
    available_cols = [col for col in feature_cols if col in df.columns]
    chart = alt.Chart(df).mark_circle().encode( 
        x=alt.X('selmer_rank:Q', title='Rank'), 
        y=alt.Y('betti_1:Q', title='Betti Number (H1)'), 
        color='generator_type:N', 
        size='entropy_gradient:Q', 
        tooltip=['objid', 'logmass', 'petrorad_r', 'selmer_rank', 'selmer_status', 'entropy', 'betti_1', 'entropy_gradient'] 
    ).interactive().properties( 
        width=800, height=400, title='Rank vs. Cohomology (Betti_1) by Generator Type and Entropy Gradient' 
    ) 
    chart.save(f'{OUTPUT_PLOT_PREFIX}_interactive_scatter_cohomology.html') 
    fig = px.scatter_3d( 
        df, x='logmass', y='entropy', z='betti_1', 
        color='generator_type', size='entropy_gradient', 
        hover_data=['objid', 'selmer_rank', 'selmer_status', 'entropy', 'betti_1', 'entropy_gradient'], 
        title='3D Galaxy Features with Cohomology and Entropy Gradient' 
    ) 
    fig.write_html(f'{OUTPUT_PLOT_PREFIX}_3d_scatter_cohomology.html') 
    if gudhi is not None: 
        X_coords = df[['ra', 'dec', 'z', 'entropy']].dropna() 
        if not X_coords.empty: 
            if len(X_coords) > MAX_COHOM_POINTS:
                X_coords = X_coords.sample(MAX_COHOM_POINTS, random_state=42)
            points = X_coords[['ra', 'dec', 'z']].values
            scaler = StandardScaler()
            points = scaler.fit_transform(points)
            dist = cdist(points, points) 
            weights = X_coords['entropy'].values
            weights = np.where(np.isfinite(weights), weights, np.median(weights[np.isfinite(weights)]))
            w_rips = WeightedRipsComplex(distance_matrix=dist, weights=weights) 
            simplex_tree = w_rips.create_simplex_tree(max_dimension=2) 
            persistence = simplex_tree.persistence() 
            plot_persistence_diagram(persistence) 
            plt.title('Persistence Diagram for Galaxy Coordinates (Entropy-Weighted)') 
            plt.savefig(f'{OUTPUT_PLOT_PREFIX}_persistence_diagram.png') 
            plt.close() 
    plt.figure(figsize=(10, 6)) 
    sns.scatterplot(data=df, x='entropy_gradient', y='betti_1', hue='generator_type', size='selmer_rank') 
    plt.title('Entropy Gradient vs. Betti_1 by Generator Type') 
    plt.savefig(f'{OUTPUT_PLOT_PREFIX}_entropy_gradient_betti1.png') 
    plt.close() 
    X_valid = df[available_cols].dropna() 
    if not X_valid.empty: 
        tsne = TSNE(n_components=2, random_state=42, n_jobs=-1) 
        X_tsne = tsne.fit_transform(X_valid) 
        df_tsne = pd.DataFrame(X_tsne, columns=['TSNE1', 'TSNE2'], index=X_valid.index) 
        df_tsne['generator_type'] = df.loc[X_valid.index, 'generator_type'] 
        plt.figure(figsize=(10, 6)) 
        sns.scatterplot(data=df_tsne, x='TSNE1', y='TSNE2', hue='generator_type') 
        plt.title('t-SNE of Galaxy Features with Cohomology and Entropy Gradient') 
        plt.savefig(f'{OUTPUT_PLOT_PREFIX}_tsne_scatter_cohomology.png') 
        plt.close() 
    if not df.empty: 
        fig, ax = plt.subplots() 
        def animate(i): 
            ax.clear() 
            bin_df = df[(df['logmass'] > i) & (df['logmass'] <= i+1)] 
            sns.scatterplot(data=bin_df, x='entropy_gradient', y='betti_1', ax=ax) 
            ax.set_title(f'Entropy Gradient vs Betti_1 (logmass bin {i}-{i+1})') 
        anim = animation.FuncAnimation(fig, animate, frames=range(8,13), interval=500) 
        anim.save(f'{OUTPUT_PLOT_PREFIX}_entropy_gradient_video.mp4', writer='ffmpeg') 
        plt.close() 
    
    manifold_summary = visualize_3d_manifold(df)
    
    summary = {'Plots Generated': [
        'interactive_scatter_cohomology.html',
        '3d_scatter_cohomology.html',
        'entropy_gradient_betti1.png',
        'tsne_scatter_cohomology.png',
        'entropy_gradient_video.mp4'
    ]}
    if gudhi is not None:
        summary['Plots Generated'].append('persistence_diagram.png')
        summary['Plots Generated'].append(manifold_summary.get('Manifold Video', ''))
