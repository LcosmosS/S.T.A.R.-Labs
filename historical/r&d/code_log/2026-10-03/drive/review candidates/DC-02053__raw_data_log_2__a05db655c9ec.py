# Instead of 0.1 * median of nearest neighbor:
# Use the distance to the k-th neighbor (k=25) to ensure 
# the local graph is connected enough to potentially have a loop.
nn = NearestNeighbors(n_neighbors=k).fit(coords)
distances, indices = nn.kneighbors(coords)


# The 'max_edge_length' should be roughly the distance 
# required to bridge the gap to the 'k-th' neighbor.
adaptive_scale = np.percentile(distances[:, -1], 50) 
print(f"   {name} adaptive max_edge_length = {adaptive_scale:.2f} Mpc")
