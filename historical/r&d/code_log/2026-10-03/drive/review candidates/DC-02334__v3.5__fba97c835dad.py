        points = self.df[['x', 'y', 'z']].values
        weights = self.df['final_weight'].values
        
        # Weighted Alpha Complex (Power Complex)
        alpha = gudhi.AlphaComplex(points=points, weights=weights)
        st = alpha.create_simplex_tree()
        st.compute_persistence()
        
        return st


    def calculate_persistence_entropy(self, simplex_tree):
        """
        Quantifies the 'Heat of Expansion' (Arithmetic Thermodynamics).
