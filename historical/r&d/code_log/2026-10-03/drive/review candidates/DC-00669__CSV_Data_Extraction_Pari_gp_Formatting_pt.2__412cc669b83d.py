# Handle missing values by filling with column means
required_columns = ['logmass', 'z', 'sfr']
for col in required_columns:
    if col not in df.columns:
        print(f"Error: Missing column '{col}' in the dataset.")
        exit(1)
    df[col] = df[col].fillna(df[col].mean())


# Step 2: Define the Cosmological L-Function
# Bin SFR values to create discrete counts for the L-function
sfr_bins = np.linspace(df['sfr'].min(), df['sfr'].max(), num=50)
df['sfr_bin'] = pd.cut(df['sfr'], bins=sfr_bins, labels=False)
bin_counts = df['sfr_bin'].value_counts().sort_index()


# Define the L-function as a sum over bin counts
def l_function(s, bin_counts):
    n = np.arange(1, len(bin_counts) + 1)
    return np.sum(bin_counts.values * n**(-s))


# Step 3: Analyze the L-Function Near s=1
# Compute L(1) and an approximation of the derivative at s=1
l_1 = l_function(1, bin_counts)
l_1_01 = l_function(1.01, bin_counts)
dl_ds = (l_1_01 - l_1) / 0.01  # Approximate derivative


# Hypothesize the order of the zero based on the derivative
if abs(dl_ds) > 1e-5:
    order = 1  # First-order zero
else:
    order = 2  # Higher-order zero
print(f"Estimated order of zero at s=1: {order}")


# Step 4: Derive the SFR Formula
# Use the L-function value at s=1 to adjust the SFR prediction
def predict_sfr(logmass, z, l_value, order):
    """
    Predict SFR using a formula inspired by the BSD framework.
