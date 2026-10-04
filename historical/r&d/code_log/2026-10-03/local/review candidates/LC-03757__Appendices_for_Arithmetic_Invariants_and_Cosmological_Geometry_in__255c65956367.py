        S = KB * np.log(T_proxy / (rho_proxy ** (2/3)))
        return S
    except:
        return np.nan

# --- 7. KDE for Rank and L-Function ---
def compute_kde_features(df, rank_col='selmer_rank', lfunc_col='var_ap'):
    log_function("compute_kde_features")
    X_kde = df[[rank_col, lfunc_col]].dropna()
    if X_kde.empty:
        print("compute_kde_features: No valid data for KDE")
        return df, np.zeros(len(df))
    kde = KernelDensity(kernel='gaussian', bandwidth=0.5).fit(X_kde)
    log_dens = kde.score_samples(X_kde)
    df_kde = pd.DataFrame({f'kde_{rank_col}_{lfunc_col}': log_dens},
index=X_kde.index)
    df = df.join(df_kde)
    df[f'kde_{rank_col}_{lfunc_col}'] = df[f'kde_{rank_col}_{lfunc_col}'].fillna(0)
    print(f"compute_kde_features: Added KDE density for {rank_col} and {lfunc_col}")
    return df, log_dens

# --- 8. Scientific Derivation Functions ---
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

# --- 9. Elliptic Curve Calculations ---
@parallel
def compute_3selmer_rank(delta, conductor, logmass, entropy, pari):
    log_function("compute_3selmer_rank")
    if not all(np.isfinite(x) for x in [delta, conductor, logmass, entropy]):
        print(f"compute_3selmer_rank: Skipped - Invalid delta={delta},
conductor={conductor}, logmass={logmass}, entropy={entropy}")
