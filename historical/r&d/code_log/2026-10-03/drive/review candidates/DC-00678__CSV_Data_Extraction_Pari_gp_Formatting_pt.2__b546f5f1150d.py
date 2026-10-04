# Ensure required columns exist and handle missing values
required_columns = ['logmass', 'z', 'sfr']
optional_columns = ['petrorad_r', 'environment']  # Additional physical factors
for col in required_columns + optional_columns:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].mean())
    else:
        print(f"Warning: Column '{col}' not found. Setting to 0.")
        df[col] = 0


# Step 2: Enhance the L-Function
# Create 2D bins for mass and redshift to capture multidimensional distribution
mass_bins = np.linspace(df['logmass'].min(), df['logmass'].max(), num=25)
z_bins = np.linspace(df['z'].min(), df['z'].max(), num=25)
df['mass_bin'] = pd.cut(df['logmass'], bins=mass_bins, labels=False)
df['z_bin'] = pd.cut(df['z'], bins=z_bins, labels=False)


# Compute counts for each (mass, z) bin combination
bin_counts = df.groupby(['mass_bin', 'z_bin']).size().reset_index(name='count')
bin_counts['index'] = bin_counts.index + 1  # Create a 1D index for L-function


def l_function(s, bin_counts):
    n = bin_counts['index'].astype(float)
    a_n = bin_counts['count']
    return np.sum(a_n * n**(-s))


# Step 3: Analyze the L-Function Near s=1
l_1 = l_function(1, bin_counts)
l_1_01 = l_function(1.01, bin_counts)
dl_ds = (l_1_01 - l_1) / 0.01  # Approximate derivative


# Estimate the rank
if abs(dl_ds) > 1e-5:
    order = 1
else:
    order = 2
print(f"Estimated order of zero at s=1: {order} (Rank analogy)")


# Step 4: Derive the SFR Formula with Additional Factors
def predict_sfr(logmass, z, l_value, order, petrorad_r=0, environment=0):
    """
    SFR prediction formula with additional physical factors:
