# Define bins for SFR
sfr_bins = np.linspace(df['sfr'].min(), df['sfr'].max(), num=50)
df['sfr_bin'] = pd.cut(df['sfr'], bins=sfr_bins, labels=False)


# Calculate bin counts
bin_counts = df['sfr_bin'].value_counts().sort_index()


# Define the L-function
def l_function(s, bin_counts):
    n = np.arange(1, len(bin_counts) + 1)
    return np.sum(bin_counts.values * n**(-s))
