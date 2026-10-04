import pandas as pd
import numpy as np
from pysr import PySRRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import os  # For saving files


# Create output dir
os.makedirs("visualizations", exist_ok=True)


# Step 1: Load/Clean
df = pd.read_csv("1760769987443A.csv")
df.replace(-9999, np.nan, inplace=True)
key_cols = ['z', 'Fg', 'Fr', 'Fz', 'EBV', 'plx', 'pmRA', 'pmDE']
df.dropna(subset=key_cols, inplace=True)
df = df[(df['Fg'] > 0) & (df['Fr'] > 0) & (df['Fz'] > 0)]


# Features
df['flux_gr'] = df['Fg'] / df['Fr']
df['flux_rz'] = df['Fr'] / df['Fz']
df['log_EBV'] = np.log(df['EBV'] + 1e-6)
df['pm_mag'] = np.sqrt(df['pmRA']**2 + df['pmDE']**2)


X = df[['Fg', 'Fr', 'Fz', 'EBV', 'plx', 'pmRA', 'pmDE', 'flux_gr', 'flux_rz', 'log_EBV', 'pm_mag']]
y = df['z']


# Regime split
df_gal = df[df['z'] < 0.1]
df_clust = df[df['z'] >= 0.1]


# Function for regime regression
def run_pysr(X, y, regime):
    model = PySRRegressor(
        niterations=200,
        binary_operators=["+", "-", "*", "/", "pow"],
        unary_operators=["log", "exp", "sqrt"],
        extra_sympy_mappings={'inv': lambda x: 1/x},
        elementwise_loss="loss(prediction, target) = (prediction - target)^2",  # Fixed
        model_selection="best",
        complexity_of_operators={"pow": 3, "exp": 2, "log": 2},
        maxsize=25,
        maxdepth=5,
        parsimony=0.01,
        random_state=42,
        deterministic=True,  # Fixed for reproducibility
        parallelism='serial'
    )
    model.fit(X, y)
    return model


# Train/test per regime
for regime, dfr in [('galactic', df_gal), ('cluster', df_clust)]:
    if len(dfr) < 2: continue
    Xr = dfr[['Fg', 'Fr', 'Fz', 'EBV', 'plx', 'pmRA', 'pmDE', 'flux_gr', 'flux_rz', 'log_EBV', 'pm_mag']]
    yr = dfr['z']
    X_train, X_test, y_train, y_test = train_test_split(Xr, yr, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = run_pysr(X_train_scaled, y_train)
    best_eq = model.sympy()
    print(f"{regime.capitalize()} Best Equation:", best_eq)
    
    y_pred = model.predict(X_test_scaled)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"{regime.capitalize()} R²: {r2:.4f}, MAE: {mae:.4f}")


    # Visualization: Save scatter as PNG
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=X_test['flux_gr'], y=y_pred, hue=X_test['EBV'], palette='viridis')
    plt.title(f'{regime.capitalize()} Symbolic Projection: Flux g/r vs Predicted z')
    plt.xlabel('g/r Flux Ratio')
    plt.ylabel('Predicted z')
    plt.colorbar(label='EBV (Entropy Proxy)')
    plt.savefig(f"visualizations/{regime}_projection_scatter.png")
    plt.close()


    # 3D Interactive: Save as HTML
    fig = go.Figure(data=go.Scatter3d(
        x=X_test['flux_gr'], y=X_test['flux_rz'], z=y_pred,
        mode='markers', marker=dict(size=5, color=y_pred, colorscale='Viridis', showscale=True, colorbar_title='Predicted z')
    ))
    fig.update_layout(title=f'{regime.capitalize()} Symbolic Manifold (Flux Ratios vs Predicted z)',
                      scene=dict(xaxis_title='g/r Flux', yaxis_title='r/z Flux', zaxis_title='Predicted z'))
    fig.write_html(f"visualizations/{regime}_manifold_3d.html")
