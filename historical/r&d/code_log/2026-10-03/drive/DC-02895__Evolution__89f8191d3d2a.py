import pandas as pd
import numpy as np
from pysr import PySRRegressor  # Symbolic Regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns


# Step 1: Load and Explore the CSV Data
# Load the CSV (replace with your actual path if needed)
df = pd.read_csv("1760769987443A.csv")


# Display basic info and head to understand structure
print("DataFrame Info:")
df.info()
print("\nFirst 5 Rows:")
print(df.head())


# Handle missing or invalid values (e.g., -9999 or NaN)
# Replace placeholders like -9999 with NaN
df.replace(-9999, np.nan, inplace=True)


# Drop rows with NaN in key columns (customize based on your target; e.g., z as target, fluxes as features)
key_columns = ['z', 'Fg', 'Fr', 'Fz', 'EBV', 'plx', 'pmRA', 'pmDE']  # Example: redshift z as target, fluxes/extinction/parallax/pm as features
df.dropna(subset=key_columns, inplace=True)


# Step 2: Feature Engineering (Symbolic/Physical Proxies)
# Create derived features inspired by ECC (e.g., symbolic entropy proxies from fluxes)
df['flux_ratio_gr'] = df['Fg'] / df['Fr']  # g/r flux ratio as curvature proxy
df['flux_ratio_rz'] = df['Fr'] / df['Fz']  # r/z flux ratio
df['log_EBV'] = np.log(df['EBV'] + 1e-6)  # Log extinction as entropy measure
df['proper_motion_mag'] = np.sqrt(df['pmRA']**2 + df['pmDE']**2)  # PM magnitude as dynamic invariant


# Filter for valid data (e.g., positive fluxes)
df = df[(df['Fg'] > 0) & (df['Fr'] > 0) & (df['Fz'] > 0)]


# Step 3: Define Target and Features for Symbolic Regression
# Example: Predict redshift z (cosmic distance proxy) from fluxes/extinction/PM (symbolic invariants)
X = df[['Fg', 'Fr', 'Fz', 'EBV', 'plx', 'pmRA', 'pmDE', 'flux_ratio_gr', 'flux_ratio_rz', 'log_EBV', 'proper_motion_mag']]
y = df['z']


# Split data for validation (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Normalize features (optional, but helps symbolic regression stability)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Step 4: Symbolic Regression with PySR
# Configure PySR for discovery of expressions (operators inspired by ECC: logs, exps for curvature/entropy)
model = PySRRegressor(
    niterations=200,
    binary_operators=["+", "-", "*", "/", "pow"],
    unary_operators=["log", "exp", "sqrt", "inv(x) = 1/x"],
    model_selection="best",
    loss="loss(prediction, target) = (prediction - target)^2",
    complexity_of_operators={"pow": 3, "exp": 2, "log": 2},
    maxsize=25,
    maxdepth=5,
    parsimony=0.01,
    random_state=42
)


# Fit the model
model.fit(X_train_scaled, y_train)


# Best discovered equation
best_eq = model.sympy()
print("Best Symbolic Equation for z:", best_eq)


# Step 5: Evaluate on Test Set
y_pred = model.predict(X_test_scaled)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
print(f"R² Score: {r2:.4f}")
print(f"MAE: {mae:.4f}")


# Step 6: Visualization (Entropy Proxy vs Predicted z)
# Example: Plot flux_ratio_gr (curvature proxy) vs predicted z (projection)
plt.figure(figsize=(10, 6))
sns.scatterplot(x=X_test['flux_ratio_gr'], y=y_pred, hue=X_test['EBV'], palette='viridis')
plt.title('Symbolic Projection: Flux Ratio (Curvature Proxy) vs Predicted Redshift')
plt.xlabel('g/r Flux Ratio')
plt.ylabel('Predicted z')
plt.colorbar(label='EBV (Entropy Measure)')
plt.savefig('symbolic_projection_plot.png')
plt.show()


# Step 7: Interpret from ECC Perspective
# Analyze equation for curvature/entropy terms (e.g., logs ~ regulators, exps ~ phases)
terms = best_eq.as_terms()
print("Discovered Terms (Symbolic Invariants):", terms)
#### Output 
