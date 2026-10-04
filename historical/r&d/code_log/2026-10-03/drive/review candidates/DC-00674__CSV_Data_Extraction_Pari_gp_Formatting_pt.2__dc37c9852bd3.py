# Ensure required columns exist and handle missing values
required_columns = ['logmass', 'z', 'sfr']
for col in required_columns:
    if col not in df.columns:
        print(f"Error: Missing column '{col}' in the dataset.")
        exit(1)
    df[col] = df[col].fillna(df[col].mean())


# Step 2: Define the Cosmological L-Function
# Bin SFR values to mimic the distribution of points, analogous to an elliptic curve
sfr_bins = np.linspace(df['sfr'].min(), df['sfr'].max(), num=50)
df['sfr_bin'] = pd.cut(df['sfr'], bins=sfr_bins, labels=False)
bin_counts = df['sfr_bin'].value_counts().sort_index()


# Define the L-function: L(s) = Σ a_n * n^(-s), where a_n is the bin count
def l_function(s, bin_counts):
    n = np.arange(1, len(bin_counts) + 1).astype(float)  # Convert to float to handle negative exponents
    return np.sum(bin_counts.values * n**(-s))


# Step 3: Analyze the L-Function Near s=1 (BSD Conjecture Inspiration)
# Compute L(1) and approximate the derivative to estimate the order of the zero
l_1 = l_function(1, bin_counts)
l_1_01 = l_function(1.01, bin_counts)
dl_ds = (l_1_01 - l_1) / 0.01  # Approximate derivative


# Estimate the rank (number of independent SFR drivers) based on the zero's order
if abs(dl_ds) > 1e-5:
    order = 1  # First-order zero: one dominant factor
else:
    order = 2  # Higher-order zero: multiple factors
print(f"Estimated order of zero at s=1: {order} (Rank analogy)")


# Step 4: Derive the SFR Formula
# SFR = f(M, z) * g(L(s=1)), inspired by BSD's link between L-function and rank
def predict_sfr(logmass, z, l_value, order):
    """
    SFR prediction formula:
