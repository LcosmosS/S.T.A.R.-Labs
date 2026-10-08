import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Step 1: Load and Preprocess Data
csv_file = 'Stellar_Mass2_Table_cleaned.csv'
try:
    df = pd.read_csv(csv_file)
    print(f"Loaded '{csv_file}' successfully.")
except FileNotFoundError:
    print(f"Error: '{csv_file}' not found.")
    exit(1)

# Handle missing values and ensure required columns
required_columns = ['logmass', 'z', 'sfr']
optional_columns = ['ra', 'dec', 'petrorad_r']
for col in required_columns + optional_columns:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].mean())
    else:
        print(f"Warning: Column '{col}' not found. Setting to 0.")
        df[col] = 0

# Calculate environmental density using transform
if 'ra' in df.columns and 'dec' in df.columns:
    df['environment'] = df.groupby(['ra', 'dec'])['ra'].transform('size')
else:
    print("Warning: 'ra' and 'dec' not found. Setting 'environment' to 0.")
    df['environment'] = 0

# Step 2: Enhance the L-Function with 3D Bins
mass_bins = np.linspace(df['logmass'].min(), df['logmass'].max(), num=25)
z_bins = np.linspace(df['z'].min(), df['z'].max(), num=25)
petrorad_bins = np.linspace(df['petrorad_r'].min(), df['petrorad_r'].max(), num=25)
df['mass_bin'] = pd.cut(df['logmass'], bins=mass_bins, labels=False)
df['z_bin'] = pd.cut(df['z'], bins=z_bins, labels=False)
df['petrorad_bin'] = pd.cut(df['petrorad_r'], bins=petrorad_bins, labels=False)

# Compute bin counts
bin_counts = df.groupby(['mass_bin', 'z_bin', 'petrorad_bin']).size().reset_index(name='count')
bin_counts['index'] = bin_counts.index + 1

def l_function(s, bin_counts):
    n = bin_counts['index'].astype(float)
    a_n = bin_counts['count'] * bin_counts['index']
    return np.sum(a_n * n**(-s))

# Step 3: Analyze L-Function Near s=1
l_1 = l_function(1, bin_counts)
l_1_01 = l_function(1.01, bin_counts)
dl_ds = (l_1_01 - l_1) / 0.01
order = 2 if abs(dl_ds) < 1e-5 else 1
print(f"Estimated order of zero at s=1: {order}")

# Step 4: SFR Prediction Features
def predict_sfr_features(row, l_value, order):
    features = [row['logmass'], row['z'], l_value, row['dec'], row['petrorad_r'], row['environment'], row['logmass'] * row['z']]
    if order == 2:
        features.insert(3, l_value**2)
    return features

# Prepare data for regression
X = np.array([predict_sfr_features(row, l_1, order) for _, row in df.iterrows()])
y = df['sfr'].values

# Step 5: Cross-Validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)
mse_list = []
model = RandomForestRegressor(n_estimators=100, random_state=42)

for fold, (train_idx, test_idx) in enumerate(kf.split(X)):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mse_list.append(mse)
    print(f"Fold {fold+1} MSE: {mse:.4f}")

# Report results
print(f"\nAverage MSE: {np.mean(mse_list):.4f}")
print(f"Standard Deviation of MSE: {np.std(mse_list):.4f}")

# Step 6: Diagnostic Plots
df['predicted_sfr'] = model.predict(X)
plt.scatter(df['sfr'], df['predicted_sfr'], alpha=0.5)
plt.plot([df['sfr'].min(), df['sfr'].max()], [df['sfr'].min(), df['sfr'].max()], 'r--')
plt.xlabel('Observed SFR')
plt.ylabel('Predicted SFR')
plt.title('Observed vs. Predicted SFR')
plt.savefig('observed_vs_predicted_sfr.png')
plt.close()

residuals = df['sfr'] - df['predicted_sfr']
plt.scatter(df['logmass'], residuals, alpha=0.5)
plt.axhline(0, color='r', linestyle='--')
plt.xlabel('Logmass')
plt.ylabel('Residuals')
plt.title('Residuals vs. Logmass')
plt.savefig('residuals_vs_logmass.png')
plt.close()

plt.scatter(df['z'], residuals, alpha=0.5)
plt.axhline(0, color='r', linestyle='--')
plt.xlabel('Redshift (z)')
plt.ylabel('Residuals')
plt.title('Residuals vs. z')
plt.savefig('residuals_vs_z.png')
plt.close()

print("Saved diagnostic plots: 'observed_vs_predicted_sfr.png', 'residuals_vs_logmass.png', 'residuals_vs_z.png'")
print("Script completed successfully!")