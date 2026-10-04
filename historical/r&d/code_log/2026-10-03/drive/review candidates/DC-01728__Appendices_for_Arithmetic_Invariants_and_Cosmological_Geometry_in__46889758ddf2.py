import pandas as pd
import numpy as np
from pysr import PySRRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor  # Classifier and boosting
from xgboost import XGBRegressor  # XGBoost
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib import cm


os.makedirs("visualizations", exist_ok=True)
chunksize = 10000  # Process in chunks for large CSV


# Function to process chunk
def process_chunk(chunk):
    chunk.replace(-9999, np.nan, inplace=True)
    key_cols = ['z', 'Fg', 'Fr', 'Fz', 'EBV', 'plx', 'pmRA', 'pmDE']
    chunk.dropna(subset=key_cols, inplace=True)
    chunk = chunk[(chunk['Fg'] > 0) & (chunk['Fr'] > 0) & (chunk['Fz'] > 0)]
    
    chunk['flux_gr'] = chunk['Fg'] / chunk['Fr']
    chunk['flux_rz'] = chunk['Fr'] / chunk['Fz']
    chunk['log_EBV'] = np.log(chunk['EBV'] + 1e-6)
    chunk['pm_mag'] = np.sqrt(chunk['pmRA']**2 + chunk['pmDE']**2)
    
    return chunk


# Load full CSV in chunks
df_list = []
for chunk in pd.read_csv("1760769987443A.csv", chunksize=chunksize):
    processed = process_chunk(chunk)
    if not processed.empty:
        df_list.append(processed)
df = pd.concat(df_list, ignore_index=True)
print("Processed Data Info:", df.info())


# Classifier for regime (train on z threshold as label)
df['regime_label'] = (df['z'] >= 0.1).astype(int)  # 0 galactic, 1 cluster
X_clf = df[['Fg', 'Fr', 'Fz', 'EBV', 'plx', 'pmRA', 'pmDE', 'flux_gr', 'flux_rz', 'log_EBV', 'pm_mag']]
y_clf = df['regime_label']
X_clf_train, X_clf_test, y_clf_train, y_clf_test = train_test_split(X_clf, y_clf, test_size=0.2, random_state=42)
clf = RandomForestClassifier(random_state=42)
clf.fit(X_clf_train, y_clf_train)
clf_acc = clf.score(X_clf_test, y_clf_test)
print("Regime Classifier Accuracy:", clf_acc)


# Predict regimes to balance if needed
df['predicted_regime'] = clf.predict(X_clf)


# Regime split using predicted (for robustness)
df_gal = df[df['predicted_regime'] == 0]
df_clust = df[df['predicted_regime'] == 1]


imputer = SimpleImputer(strategy='mean')


# PySR and Boosting per regime
def run_models(X, y, regime):
    X = imputer.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # PySR
    pysr_model = PySRRegressor(
        niterations=200,
        binary_operators=["+", "-", "*", "/", "pow"],
        unary_operators=["log", "exp", "sqrt"],
        extra_sympy_mappings={'inv': lambda x: 1/x},
        elementwise_loss="loss(prediction, target) = (prediction - target)^2",
        model_selection="best",
        complexity_of_operators={"pow": 3, "exp": 2, "log": 2},
        maxsize=25,
        maxdepth=5,
        parsimony=0.01,
        random_state=42,
        deterministic=True,
        parallelism='serial',
        constraints={'^': (-1, 1)}
    )
    pysr_model.fit(X_train_scaled, y_train)
    pysr_eq = pysr_model.sympy()
    y_pred_pysr = pysr_model.predict(X_test_scaled)
    r2_pysr = r2_score(y_test, y_pred_pysr)
    mae_pysr = mean_absolute_error(y_test, y_pred_pysr)


    # XGBoost Boosting
    xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=5, random_state=42)
    xgb_model.fit(X_train_scaled, y_train)
    y_pred_xgb = xgb_model.predict(X_test_scaled)
    r2_xgb = r2_score(y_test, y_pred_xgb)
    mae_xgb = mean_absolute_error(y_test, y_pred_xgb)
    
    print(f"{regime.capitalize()} PySR Eq:", pysr_eq)
    print(f"{regime.capitalize()} PySR R²: {r2_pysr:.4f}, MAE: {mae_pysr:.4f}")
    print(f"{regime.capitalize()} XGBoost R²: {r2_xgb:.4f}, MAE: {mae_xgb:.4f}")
    
    return pysr_model, xgb_model, X_test, y_pred_pysr, y_pred_xgb


# Run for regimes
for regime, dfr in [('galactic', df_gal), ('cluster', df_clust)]:
    if len(dfr) < 2: continue
    Xr = dfr[['Fg', 'Fr', 'Fz', 'EBV', 'plx', 'pmRA', 'pmDE', 'flux_gr', 'flux_rz', 'log_EBV', 'pm_mag']]
    yr = dfr['z']
    pysr_model, xgb_model, X_test, y_pred_pysr, y_pred_xgb = run_models(Xr, yr, regime)
    
    # Visuals (use X_test as DF for columns)
    X_test_df = pd.DataFrame(X_test, columns=Xr.columns)  # Reconstruct DF
    
    # PNG Scatter
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(X_test_df['flux_gr'], y_pred_pysr, c=X_test_df['EBV'], cmap=cm.viridis)
    ax.set_title(f'{regime.capitalize()} PySR Projection: g/r Flux vs Predicted z')
    ax.set_xlabel('g/r Flux Ratio')
    ax.set_ylabel('Predicted z')
    fig.colorbar(scatter, label='EBV (Entropy Proxy)')
    fig.savefig(f"visualizations/{regime}_pysr_scatter.png")
    plt.close(fig)
    
    # HTML 3D for PySR
    fig = go.Figure(data=go.Scatter3d(
        x=X_test_df['flux_gr'], y=X_test_df['flux_rz'], z=y_pred_pysr,
        mode='markers', marker=dict(size=5, color=y_pred_pysr, colorscale='Viridis', showscale=True, colorbar_title='Predicted z')
    ))
    fig.update_layout(title=f'{regime.capitalize()} PySR Manifold',
                      scene=dict(xaxis_title='g/r Flux', yaxis_title='r/z Flux', zaxis_title='Predicted z'))
    fig.write_html(f"visualizations/{regime}_pysr_manifold_3d.html")
