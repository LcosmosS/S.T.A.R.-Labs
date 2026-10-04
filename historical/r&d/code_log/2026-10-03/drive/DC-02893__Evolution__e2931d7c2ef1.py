import pandas as pd
import numpy as np
from pysr import PySRRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
import sympy as sp  # For ψ/volume if needed


# Step 1: Load and Clean CSV
df = pd.read_csv("1760769987443A.csv")
print("Data Info:", df.info())
df.replace(-9999, np.nan, inplace=True)
key_cols = ['z', 'Fg', 'Fr', 'Fz', 'EBV', 'plx', 'pmRA', 'pmDE']  # Target z, features
df.dropna(subset=key_cols, inplace=True)
df = df[(df['Fg'] > 0) & (df['Fr'] > 0) & (df['Fz'] > 0)]


# Step 2: Feature Engineering (ECC-inspired: ratios~curvature, logs~entropy)
df['flux_gr'] = df['Fg'] / df['Fr']
df['flux_rz'] = df['Fr'] / df['Fz']
df['log_EBV'] = np.log(df['EBV'] + 1e-6)
df['pm_mag'] = np.sqrt(df['pmRA']**2 + df['pmDE']**2)


X = df[['Fg', 'Fr', 'Fz', 'EBV', 'plx', 'pmRA', 'pmDE', 'flux_gr', 'flux_rz', 'log_EBV', 'pm_mag']]
y = df['z']


# Split and Scale
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Step 3: PySR with Fixed Mappings (Fix Error: Add SymPy for 'inv')
model = PySRRegressor(
    niterations=200,
    binary_operators=["+", "-", "*", "/", "pow"],
    unary_operators=["log", "exp", "sqrt"],
    extra_sympy_mappings={'inv': lambda x: 1/x},  # Fixed: Define SymPy for inv
    model_selection="best",
    loss="loss(prediction, target) = (prediction - target)^2",
    complexity_of_operators={"pow": 3, "exp": 2, "log": 2},
    maxsize=25,
    maxdepth=5,
    parsimony=0.01,
    random_state=42
)


model.fit(X_train_scaled, y_train)
best_eq = model.sympy()
print("Best Equation for z:", best_eq)


# Evaluate
y_pred = model.predict(X_test_scaled)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
print(f"R²: {r2:.4f}, MAE: {mae:.4f}")


# Step 4: 3D Visualization (Like Your Images: Manifold of Projections)
fig = go.Figure(data=go.Scatter3d(
    x=X_test['flux_gr'], y=X_test['flux_rz'], z=y_pred,
    mode='markers', marker=dict(size=5, color=y_pred, colorscale='Viridis', showscale=True, colorbar_title='Predicted z')
))
fig.update_layout(title="Symbolic Projection Manifold (Flux Ratios vs Predicted z)",
                  scene=dict(xaxis_title='g/r Flux', yaxis_title='r/z Flux', zaxis_title='Predicted z'))
fig.show()
fig.write_html("symbolic_manifold.html")  # Save interactive HTML


# Optional: Integrate ψ/Volume (Mock Ranks from Data, e.g., from Flux Clusters)
df['mock_rank'] = pd.cut(df['z'], bins=3, labels=[1,2,3])  # Proxy ranks from z
# ... (add ψ calc as in psi.py)
