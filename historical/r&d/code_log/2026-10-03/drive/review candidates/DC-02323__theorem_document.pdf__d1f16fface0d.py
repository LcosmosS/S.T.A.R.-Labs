from scipy.spatial.stats import correlation
# Compute correlation function
corr = correlation(galaxy_data['positions'])
# Calculate power spectrum
power = np.fft.fft(corr)
return {
'correlation': corr,
'power_spectrum': power
