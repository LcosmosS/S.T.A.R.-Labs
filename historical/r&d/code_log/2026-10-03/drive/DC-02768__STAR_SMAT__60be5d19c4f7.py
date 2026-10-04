        self.points = points
        # Use log-scaling for the mass proxy to prevent extreme outliers from collapsing the topology
        # We add 1e-8 to avoid log(0) in case of exact 0 values
        self.log_mass = np.log(np.abs(mass_proxy) + 1e-8)
        
        # Scale weights into a reasonable range relative to spatial distances
        scaler = MinMaxScaler(feature_range=(0.1, 5.0)) 
        self.weights = scaler.fit_transform(self.log_mass.reshape(-1, 1)).flatten()


    def alternative_a_weighted_alpha_complex(self):
        """
        Alternative A: Power/Alpha Complex
