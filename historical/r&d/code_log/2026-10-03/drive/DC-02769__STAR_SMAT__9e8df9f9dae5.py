        print("Building Weighted Alpha (Power) Complex...")
        # Gudhi's AlphaComplex natively accepts weights for a power distance complex
        alpha_complex = gudhi.AlphaComplex(points=self.points, weights=self.weights)
        
        simplex_tree = alpha_complex.create_simplex_tree()
        simplex_tree.compute_persistence()
        
        # Return the persistence diagram
        return simplex_tree.persistence()


    def alternative_b_density_cubical_complex(self, grid_resolution=20):
        """
        Alternative B: Continuous Density Field (KDE) + Cubical Complex
