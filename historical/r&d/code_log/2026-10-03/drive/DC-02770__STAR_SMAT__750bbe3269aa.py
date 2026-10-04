        print(f"Building Weighted KDE Field at {grid_resolution}^3 resolution...")
        
        # 1. Define the 3D grid boundaries based on the point cloud
        x_min, x_max = self.points[:, 0].min(), self.points[:, 0].max()
        y_min, y_max = self.points[:, 1].min(), self.points[:, 1].max()
        z_min, z_max = self.points[:, 2].min(), self.points[:, 2].max()
        
        # Create the grid
        x_grid = np.linspace(x_min, x_max, grid_resolution)
        y_grid = np.linspace(y_min, y_max, grid_resolution)
        z_grid = np.linspace(z_min, z_max, grid_resolution)
        X, Y, Z = np.meshgrid(x_grid, y_grid, z_grid, indexing='ij')
        grid_coords = np.vstack([X.ravel(), Y.ravel(), Z.ravel()])
        
        # 2. Compute the Weighted Kernel Density Estimate
        # The points are weighted by their log-scaled arithmetic mass
        kde = gaussian_kde(self.points.T, weights=self.weights)
        
        # Evaluate density over the grid
        density = kde(grid_coords).reshape(grid_resolution, grid_resolution, grid_resolution)
        
        # 3. Superlevel Set Filtration
        # TDA typically filters from lowest to highest. We want high-density clusters 
        # to appear first (be born early), so we negate the density field.
        neg_density = -density 
        
        print("Computing Cubical Complex Persistence...")
        cubical_complex = gudhi.CubicalComplex(top_dimensional_cells=neg_density)
        cubical_complex.compute_persistence()
        
        return cubical_complex.persistence()


def test_weighted_topologies(df_arithmetic, cosmo_pc):
    """
    df_arithmetic: DataFrame containing 'x', 'y', 'z' and 'regulator'
