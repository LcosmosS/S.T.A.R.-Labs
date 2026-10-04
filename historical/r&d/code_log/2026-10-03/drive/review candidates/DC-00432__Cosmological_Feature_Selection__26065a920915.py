# Function to cross-match in chunks
def cross_match_in_chunks(df1, filepath, ra_col1, dec_col1, ra_col2, dec_col2, columns_to_keep, max_dist_arcsec=10.0, chunksize=100000): df1_cleaned = clean_coordinates(df1, ra_col1, dec_col1) if len(df1_cleaned) == 0: print("No valid data in df1 after cleaning. Cannot perform cross-match.") return df1_cleaned, pd.DataFrame()
# Get RA/Dec range of df1 with a buffer (max_dist_arcsec converted to degrees)
buffer_deg = max_dist_arcsec / 3600.0 ra_min, ra_max = df1_cleaned[ra_col1].min() - buffer_deg, df1_cleaned[ra_col1].max() + buffer_deg dec_min, dec_max = df1_cleaned[dec_col1].min() - buffer_deg, df1_cleaned[dec_col1].max() + buffer_deg print(f"Filtering df2 to RA range {ra_min:.4f} to {ra_max:.4f}, Dec range {dec_min:.4f} to {dec_max:.4f}")
# Convert df1 to radians
df1_cleaned = deg_to_rad(df1_cleaned, ra_col1, dec_col1) coords1 = np.array([df1_cleaned['ra_rad'], df1_cleaned['dec_rad']]).T
# Process df2 in chunks
matched_df1_list = [] matched_df2_list = [] chunk_reader = pd.read_csv(filepath, chunksize=chunksize) for i, chunk in enumerate(chunk_reader): print(f"Processing chunk {i+1} with {len(chunk)} rows...") # Filter chunk by RA/Dec range chunk_filtered = chunk[ (chunk[ra_col2].between(ra_min, ra_max)) & (chunk[dec_col2].between(dec_min, dec_max)) ] print(f"Chunk {i+1} after filtering: {len(chunk_filtered)} rows.") if len(chunk_filtered) == 0: continue
# Clean the chunk
chunk_cleaned = clean_coordinates(chunk_filtered, ra_col2, dec_col2)
if len(chunk_cleaned) == 0:
    continue


# Convert to radians
chunk_cleaned = deg_to_rad(chunk_cleaned, ra_col2, dec_col2)
coords2 = np.array([chunk_cleaned['ra_rad'], chunk_cleaned['dec_rad']]).T


# Perform cross-match
tree = cKDTree(coords2)
max_dist = np.radians(max_dist_arcsec / 3600.0)
dist, idx = tree.query(coords1, k=1, distance_upper_bound=max_dist)


# Filter matches
matched = dist < max_dist
if not np.any(matched):
    continue


df1_matched = df1_cleaned[matched].copy()
df2_matched = chunk_cleaned.iloc[idx[matched]].copy()


# Reset indices
df1_matched = df1_matched.reset_index(drop=True)
df2_matched = df2_matched.reset_index(drop=True)


matched_df1_list.append(df1_matched)
matched_df2_list.append(df2_matched[columns_to_keep])


# Print sample matches
print(f"Chunk {i+1} matches: {len(df1_matched)}")
if len(df1_matched) > 0:
    print("Sample matches (first 5):")
    for j in range(min(5, len(df1_matched))):
        print(f"Match {j+1}: {ra_col1}={df1_matched[ra_col1].iloc[j]:.4f}, {dec_col1}={df1_matched[dec_col1].iloc[j]:.4f} "
              f"matched to {ra_col2}={df2_matched[ra_col2].iloc[j]:.4f}, {dec_col2}={df2_matched[dec_col2].iloc[j]:.4f} "
              f"(distance={(dist[matched][j] * 3600 * 180 / np.pi):.2f} arcsec)")
# Combine all matches
if matched_df1_list: final_df1 = pd.concat(matched_df1_list).drop_duplicates(subset=['objra_y', 'objdec']).reset_index(drop=True) final_df2 = pd.concat(matched_df2_list).reset_index(drop=True) print(f"Total matches after combining chunks: {len(final_df1)}") return final_df1, final_df2 else: print("No matches found across all chunks.") return df1_cleaned, pd.DataFrame()
