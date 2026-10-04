    SAMPLE_SIZE = 250000
    SEED = int(42)
    real1 = real1.sample(SAMPLE_SIZE, random_state=SEED).reset_index(drop=True)
    real2 = real2.sample(SAMPLE_SIZE, random_state=SEED).reset_index(drop=True)
    return synth, real1, real2


synth, real1, real2 = load_data()


# ====================== 2. FORMAL ACSC + TUNABLE β ======================
class ProjectionEngine:
    def __init__(self, beta=16.263, lambda_scale=1.0):
        self.ALPHA = np.sqrt(1.5)
        self.BETA = beta
        self.LAMBDA = lambda_scale


    def apply(self, seed, t_cosmo):
        delta = getattr(seed, 'discriminant', seed.conductor * 10)
        conductor = seed.conductor
        
        # Geometry remains consistent
        theta = np.mod(np.log10(abs(delta) + 1) * 2 * np.pi, 2 * np.pi)
        phi = np.mod(np.log10(conductor + 1) * np.pi, np.pi)
        
        # --- NEW CORE LOGIC (Complexity 14 + Betti Ratio) ---
        b_ratio = seed.rank / (np.log10(conductor + 1) + 1e-8)
        
        # Discovered Equation of State
        inner_force = ((b_ratio**2 - t_cosmo) + (np.exp(t_cosmo) * 0.4032)) / 0.4610
        z_projected = self.LAMBDA * (1.0 / (np.exp(inner_force) + 1e-9))
        # ----------------------------------------------------


        x = z_projected * np.sin(phi) * np.cos(theta)
        y = z_projected * np.sin(phi) * np.sin(theta)
        z = z_projected * np.cos(phi)
        return np.array([x, y, z])


# ====================== 3. LEAKAGE-FREE FEATURES + BETTI-0 ======================


def add_thesis_features(df, target_col=None):
    df = df.copy()
    df['flux_gr'] = df.get('Gmag', 0) / (df.get('Jmag', 1) + 1e-8)
    df['pm_mag_proxy'] = np.sqrt(df.get('pmRA', 0)**2 + df.get('pmDE', 0)**2)
    df['mag_ratio'] = df.get('gmag', 0) / (df.get('rmag', 1) + 1e-8)
    
    if 'Vcmb' in df.columns:
        df['Tully_Fisher'] = df.get('gmag', 0) + 5 * np.log10(df['Vcmb'] / 100.0)
    else:
        df['Tully_Fisher'] = df.get('gmag', 0)
    
    if 'local_density' in df.columns:
        df['Anthropic'] = np.abs(df['local_density'] - df['local_density'].median())
    else:
        df['Anthropic'] = 0.0
    
    if target_col != 'zphot' and 'zphot' in df.columns:
        df['T_cosmo'] = 1.0 / (1.0 + df['zphot'])
    elif 'Vcmb' in df.columns:
        df['T_cosmo'] = 1.0 / (1.0 + df['Vcmb'] / 3e5)
    else:
        df['T_cosmo'] = 1.0
    
    for col in ['flux_gr', 'pm_mag_proxy', 'mag_ratio', 'Tully_Fisher', 'Anthropic', 'T_cosmo']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)
    return df


def add_comprehensive_proxies(df, coords, dists, indices, target_col=None):
    """
    Combines intrinsic photometric proxies with extrinsic structural geometry.
