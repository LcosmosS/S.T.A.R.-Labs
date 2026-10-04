tree = cKDTree(xyz)
dist_threshold = 1 / cosmo.hubble_distance.value  # ~1 Mpc

# Function to compute neighbors for a chunk of indices
=========================================================================================
=======================
def compute_neighbors_chunk(chunk_indices, xyz_data, dist_thr):
    local_tree = cKDTree(xyz_data)  # Rebuild tree for consistency (small overhead)
    return [len(local_tree.query_ball_point(xyz_data[i], r=dist_thr)) - 1 for i in chunk_indices]

# Parallelize the neighbor search
=========================================================================================
============================================
n_cores = mp.cpu_count()  # Use all available cores on SciServer
chunk_size = len(df) // n_cores
if chunk_size == 0:
    chunk_size = len(df)  # Handle case where n_rows < n_cores

index_chunks = [range(i, min(i + chunk_size, len(df))) for i in range(0, len(df), chunk_size)]
pool = mp.Pool(processes=n_cores)
compute_neighbors_partial = partial(compute_neighbors_chunk, xyz_data=xyz, dist_thr=dist_threshold)

# Compute neighbors in parallel
=========================================================================================
==============================================
results = pool.map(compute_neighbors_partial, index_chunks)
pool.close()
pool.join()

# Flatten the results
=========================================================================================
========================================================
cluster_density = []
for chunk_result in results:
    cluster_density.extend(chunk_result)

df['cluster_density'] = cluster_density

# Diagnostics
=========================================================================================
==============================================================================
end_time = time.time()
print(f"Clustering completed in {end_time - start_time:.2f} seconds.")
print(f"Memory usage after clustering: {df.memory_usage().sum() / 1024**2:.2f} MB")
print(f"cluster_density: mean={df['cluster_density'].mean():.2f}, std={df['cluster_density'].std():.2f}, "
      f"min={df['cluster_density'].min():.2f}, max={df['cluster_density'].max():.2f}")

# Galactic extinction correction (enhanced with caching and robust error handling)
====================================================================================