    return pd.Series({
        'reg_cosmo': reg_cosmo,
        't_cosmo': t_cosmo,
        'log_delta': np.log(abs(delta)) if np.isfinite(delta) and delta > 0 else
np.nan,
        'log_omega': np.log(abs(omega)) if np.isfinite(omega) and omega > 0 else
np.nan,
        'log_torsion': np.log(1 + torsion) if np.isfinite(torsion) else np.nan,
        'log_conductor': np.log(abs(conductor)) if np.isfinite(conductor) and
conductor > 0 else np.nan,
        'real_log_j': np.log(abs(j_invariant)) if np.isfinite(j_invariant) and
j_invariant != 0 else np.nan,
        'imag_log_j': 0.0,
        'tr_p1': tr_p1,
        'var_ap': var_ap,
        'sato_tate': sato_tate,
        'isogeny_count': isogeny_count,
        'log_min_isogeny': np.log(min_isogeny_deg) if min_isogeny_deg != 0 else
np.nan,
        'log_torsion_type': np.log(1 + torsion_type),
        'selmer_rank': selmer_rank,
        'selmer_status': selmer_status,
        'torsion': torsion,
        'j_invariant': j_inv,
        'discriminant': disc,
        'entropy': entropy
    })

# --- 11. Generator Type Classification ---
def classify_generator(row):
    log_function("classify_generator")
    if pd.isna(row['log_delta']):
        return 'unknown', False
    is_simple = abs(row['log_delta'] - round(row['log_delta'])) < 0.1
    return 'Simple' if is_simple else 'Recursive', is_simple

# --- 12. Generator Structure Analysis ---
def analyze_generator_structure(coords):
    log_function("analyze_generator_structure")
    if pd.isna(coords):
        return {'type': 'unknown', 'structure': 'unknown'}
    x, y = coords if isinstance(coords, tuple) else (np.nan, np.nan)
    if pd.isna(x) or pd.isna(y):
        return {'type': 'unknown', 'structure': 'unknown'}
    if isinstance(x, (int, float)) and isinstance(y, (int, float)) and
float(x).is_integer() and float(y).is_integer():
        return {'type': 'Simple', 'structure': 'integer'}
    denom_x = x.denominator() if hasattr(x, 'denominator') else 1