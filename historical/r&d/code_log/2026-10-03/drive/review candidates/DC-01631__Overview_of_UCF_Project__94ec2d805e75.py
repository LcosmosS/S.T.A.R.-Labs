    delta_max = max(deltas) if deltas else 1
    n_max = max(ns) if ns else 1
    log_delta_max = math.log(delta_max) if delta_max > 1 else 1
    log_n_max = math.log(n_max) if n_max > 1 else 1
    
    points = []
    for c in curves:
        if c['Delta'] > 0 and c['N'] > 0:
            log_delta = math.log(c['Delta'])
            log_n = math.log(c['N'])
            phi = (log_delta / log_delta_max) * 360
            theta = (log_n / log_n_max) * 180
            z = alpha * c['r']
            points.append([phi, theta, z])
    return np.array(points)


# Step 3: Fetch a small SDSS galaxy catalog (e.g., around Virgo Cluster for test)
def fetch_sdss_galaxies():
    # Query a small region (max radius 3 arcmin for SDSS query_region)
    pos = SkyCoord('12h30m00s +12d00m00s', frame='icrs')
    query_results = SDSS.query_region(pos, radius=2*u.arcmin, fields=['ra', 'dec', 'z'])
    if query_results is None:
        raise ValueError("No SDSS data found; check connection or install astroquery")
    df = query_results.to_pandas()
    points = df[['ra', 'dec', 'z']].to_numpy()
    # Normalize z (redshift) to arbitrary scale for comparison (e.g., multiply by 100 for distance proxy)
    points[:, 2] *= 100
    return points


# Step 4: Compute persistent homology diagram for a point cloud (H1 for loops/filaments)
def compute_persistence_diagram(points, dimension=1):
    alpha_complex = AlphaComplex(points=points)
    simplex_tree = alpha_complex.create_simplex_tree(max_alpha_square=1e12)  # Large to capture structure
    persistence = simplex_tree.persistence()
    diagram = simplex_tree.persistence_intervals_in_dimension(dimension)
    if len(diagram) == 0:
        diagram = np.array([[0, 0]])  # Fallback empty diagram
    return diagram


# Step 5: Main pipeline
def run_pipeline(max_n=50, alpha=200):
    # Generate and project elliptic curves using Sage
    curves = generate_elliptic_curves(max_n)
    elliptic_points = project_curves(curves, alpha)
    print(f"Generated {len(curves)} elliptic curves, projected to {len(elliptic_points)} points.")
    
    # Fetch SDSS galaxies
    cosmic_points = fetch_sdss_galaxies()
    print(f"Fetched {len(cosmic_points)} cosmic points from SDSS.")
    
    # Normalize both point clouds to [0,1] for fair comparison
    def normalize(points):
        mins = np.min(points, axis=0)
        maxs = np.max(points, axis=0)
        return (points - mins) / (maxs - mins + 1e-10)
    
    elliptic_points = normalize(elliptic_points)
    cosmic_points = normalize(cosmic_points)
    
    # Compute persistence diagrams (H1)
    elliptic_diag = compute_persistence_diagram(elliptic_points, dimension=1)
    cosmic_diag = compute_persistence_diagram(cosmic_points, dimension=1)
    
    # Compute Wasserstein distance (order 1, Euclidean metric)
    dist = wasserstein_distance(elliptic_diag, cosmic_diag, order=1., internal_p=2.)
    print(f"Wasserstein distance between persistence diagrams: {dist:.4f}")
    
    # For ECC test (simplified: bound topological entropy ~ log(max persistence length))
    elliptic_entropy_bound = math.log(np.max(elliptic_diag[:,1] - elliptic_diag[:,0]) + 1)
    print(f"Simplified entropy bound for elliptic diagram: {elliptic_entropy_bound:.4f}")
    
    return dist


# Run the pipeline
if __name__ == "__main__":
    run_pipeline()
 
#### Output
