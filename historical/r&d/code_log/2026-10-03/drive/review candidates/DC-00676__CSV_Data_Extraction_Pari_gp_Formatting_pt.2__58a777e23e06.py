# Ensure required columns exist and handle missing values
required_columns = ['logmass', 'z', 'sfr']
optional_columns = ['metallicity', 'environment']  # Add optional features
for col in required_columns:
    if col not in df.columns:
        print(f"Error: Missing column '{col}' in the dataset.")
        exit(1)
    df[col] = df[col].fillna(df[col].mean())


# Handle optional columns
for col in optional_columns:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].mean())
    else:
        df[col] = 0  # Placeholder if not present


# Step 2: Define the Cosmological L-Function
# Bin SFR values to mimic the distribution of points
sfr_bins = np.linspace(df['sfr'].min(), df['sfr'].max(), num=50)
df['sfr_bin'] = pd.cut(df['sfr'], bins=sfr_bins, labels=False)
bin_counts = df['sfr_bin'].value_counts().sort_index()


def l_function(s, bin_counts):
    n = np.arange(1, len(bin_counts) + 1).astype(float)
    return np.sum(bin_counts.values * n**(-s))


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


# Step 4: Derive the SFR Formula
def predict_sfr(logmass, z, l_value, order, metallicity=0, environment=0):
    """
    SFR prediction formula with additional features:
