def l_function(s, bin_counts): n = bin_counts['index'].astype(float) a_n = bin_counts['count'] * bin_counts['index'] # Weight by index return np.sum(a_n * n**(-s))
