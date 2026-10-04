import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import sympy as sp
import matplotlib.pyplot as plt
import seaborn as sns


# Load your cosmic dataset
df = pd.read_csv("pipe3d_data.csv")


# Select important features
features = ['log_Mass_gas', 'metallicity', 'dust_attenuation', 'SFR', 'stellar_mass', 'age_lightW', 'Av_ssp']
df = df[features].dropna()


# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df.drop(columns='SFR'))
y = df['SFR'].values


# PCA to project into lower-dimensional space (symbolic link to rational points)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)


# Define a symbolic form of L(cosmos)
x, y_sym = sp.symbols('x y')
L_cosmos_expr = x**3 + sp.Function('a')(x)*x + sp.Function('b')(x)


# Use a machine learning model to approximate SFR as f(log_Mass_gas, metallicity, etc)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
model = GradientBoostingRegressor()
model.fit(X_train, y_train)
score = model.score(X_test, y_test)
print(f"Model R^2 Score on SFR: {score:.4f}")


# Plot PCA projection to visualize "curve-like" galactic structure
plt.figure(figsize=(10, 7))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=df['SFR'], palette='viridis')
plt.title("PCA Projection of Galactic Features (Symbolic Rational Structure)")
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.colorbar(label='SFR')
plt.grid(True)
plt.show()


# Estimate L-function-like structure (pseudo: summing inverse SFR-like quantities)
pseudo_L = np.sum(1 / (1 + df['SFR']))
print(f"Pseudo L(cosmos): {pseudo_L:.5f}")


# Optional: Symbolic regression (using sympy) - placeholder for further refinement
log_M, Z, Av = sp.symbols('log_M Z Av')
SFR_expr = sp.lambdify((log_M, Z, Av), log_M**2 + Z*Av - log_M*Z)
print("Symbolic SFR model: SFR ≈ log_M^2 + Z*Av - log_M*Z")


# Next steps: refine SFR_expr using symbolic regression or PySR (Physics-Inspired Symbolic Regression)
