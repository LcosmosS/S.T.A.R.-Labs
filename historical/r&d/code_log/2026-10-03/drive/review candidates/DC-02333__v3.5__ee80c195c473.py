        self.df = df.copy()
        
        # 1. Log-Normalization of Invariants (Critical for KDE stability)
        # We use log10(N_E) to prevent 'blindness' where one massive conductor 
        # flattens the density field for everything else.
        self.df['log_N'] = np.log10(self.df['conductor'])
        
        # 2. The BSD-Refined Weighting Scheme
        # w_E ∝ R_E / T_E^2 (as suggested by the BSD leading term formula)
        # We use log1p to compress the range for rank 4+ curves while preserving order.
        self.df['bsd_weight'] = self.df['regulator'] / (self.df['torsion']**2 + 1e-9)
        self.df['norm_weight'] = np.log1p(self.df['bsd_weight'])
        
        # Standardize for the Alpha Complex input
        scaler = RobustScaler(quantile_range=(5, 95))
        self.df['final_weight'] = scaler.fit_transform(self.df[['norm_weight']])


    def compute_weighted_alpha_complex(self):
        """
        Computes the persistence of the 'Arithmetic Web' using the BSD-weighting.
