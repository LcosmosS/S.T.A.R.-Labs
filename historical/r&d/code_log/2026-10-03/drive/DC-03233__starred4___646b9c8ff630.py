bin_counts = df.groupby(['mass_bin', 'z_bin']).size().reset_index(name='count') bin_counts['index'] = bin_counts.index + 1 # Create a 1D index for L-function
def l_function(s, bin_counts): n = bin_counts['index'].astype(float) a_n = bin_counts['count'] return np.sum(a_n * n**(-s))
