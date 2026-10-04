        t_cosmo = 1.0 / (1.0 + redshift_slice)
        results = []
        for seed in self.seeds:
            coords = self.engine.apply(seed, t_cosmo)
            results.append({
                'label': seed.label,
                'x': coords[0], 'y': coords[1], 'z': coords[2],
                'rank': seed.rank
            })
        return pd.DataFrame(results)


    def compute_mission_fidelity(self, projected_df):
        """Calculates the ACSC Wasserstein Distance between the mission and the target."""
        if self.target_manifold is None: return None
        
        # Compare distribution of 'rank' (arithmetic) vs 'local_density' (physical)
        # This is the 'Topological Cost' of the mission
        w2_dist = wasserstein_distance(
            projected_df['rank'], 
            self.target_manifold['zphot'] # Proxy for expansion/density
