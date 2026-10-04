# Step 2: Enhance the L-Function # Create 3D bins for mass, redshift, and petrorad_r
mass_bins = np.linspace(df['logmass'].min(), df['logmass'].max(), num=25) z_bins = np.linspace(df['z'].min(), df['z'].max(), num=25) petrorad_bins = np.linspace(df['petrorad_r'].min(), df['petrorad_r'].max(), num=25) df['mass_bin'] = pd.cut(df['logmass'], bins=mass_bins, labels=False) df['z_bin'] = pd.cut(df['z'], bins=z_bins, labels=False) df['petrorad_bin'] = pd.cut(df['petrorad_r'], bins=petrorad_bins, labels=False)
# Compute counts for each (mass, z, petrorad_r) bin combination
bin_counts = df.groupby(['mass_bin', 'z_bin', 'petrorad_bin']).size().reset_index(name='count') bin_counts['index'] = bin_counts.index + 1 # Create a 1D index for L-function
def l_function(s, bin_counts): n = bin_counts['index'].astype(float) a_n = bin_counts['count'] * bin_counts['index'] # Weight by index for physical relevance return np.sum(a_n * n**(-s))
# Step 3: Analyze the L-Function Near s=1
l_1 = l_function(1, bin_counts) l_1_01 = l_function(1.01, bin_counts) dl_ds = (l_1_01 - l_1) / 0.01 # Approximate derivative
# Estimate the rank
