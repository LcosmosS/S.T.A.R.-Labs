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
