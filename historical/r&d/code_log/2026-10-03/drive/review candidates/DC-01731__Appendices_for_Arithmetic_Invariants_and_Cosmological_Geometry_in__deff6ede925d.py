import pandas as pd
import numpy as np
from pysr import PySRRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBRegressor
from imblearn.over_sampling import SMOTE
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib import cm


pd.set_option('mode.chained_assignment', None)
os.makedirs("visualizations", exist_ok=True)
chunksize = 10000


# Process chunk
def process_chunk(chunk):
    chunk = chunk.copy()
    chunk.replace(-9999, np.nan, inplace=True)
    key_cols = ['z', 'Fg', 'Fr', 'Fz', 'EBV', 'plx', 'pmRA', 'pmDE', 'Chi2', 'delChi2', 'TSNR2_ELG', 'TSNR2_LRG', 'Morph', 'OType']
    chunk = chunk.dropna(subset=key_cols)
    chunk = chunk[(chunk['Fg'] > 0) & (chunk['Fr'] > 0) & (chunk['Fz'] > 0)]
    
    coeff_cols = [col for col in chunk.columns if col.startswith('COEFF')]
    if coeff_cols:
        chunk['coeff_sum'] = chunk[coeff_cols].sum(axis=1)
        chunk['coeff_mean'] = chunk[coeff_cols].mean(axis=1)
    
    chunk['flux_gr'] = chunk['Fg'] / chunk['Fr']
    chunk['flux_rz'] = chunk['Fr'] / chunk['Fz']
    chunk['log_EBV'] = np.log(chunk['EBV'] + 1e-6)
    chunk['pm_mag'] = np.sqrt(chunk['pmRA']**2 + chunk['pmDE']**2)
    chunk['log_chi2'] = np.log(chunk['Chi2'] + 1e-6)
    chunk['chi_ratio'] = chunk['Chi2'] / (chunk['delChi2'] + 1e-6)
    chunk['tsnr_ratio_elg_lrg'] = chunk['TSNR2_ELG'] / (chunk['TSNR2_LRG'] + 1e-6)
    
    chunk['morph_int'] = chunk['Morph'].apply(lambda x: 0 if 'GALAXY' in str(x) else 1)
    chunk['otype_int'] = chunk['OType'].apply(lambda x: 0 if 'GALAXY' in str(x) else 1)
    
    for col in chunk.select_dtypes(include=[np.number]).columns:
        chunk[col] = np.clip(chunk[col], -1e10, 1e10)
        
    return chunk


# Load chunks
df_list = []
for chunk in pd.read_csv("1760769987443A.csv", chunksize=chunksize):
    processed = process_chunk(chunk)
    if not processed.empty:
        df_list.append(processed)
df = pd.concat(df_list, ignore_index=True)
print("Full Data Info:", df.info())


imputer = SimpleImputer(strategy='mean')


# Regime Classifier
df['regime_label'] = (df['z'] >= 0.1).astype(int)
X_clf_cols = ['Fg', 'Fr', 'Fz', 'EBV', 'plx', 'pmRA', 'pmDE', 'flux_gr', 'flux_rz', 'log_EBV', 'pm_mag', 'coeff_sum', 'chi_ratio', 'tsnr_ratio_elg_lrg', 'morph_int', 'otype_int']
X_clf = df[X_clf_cols]
X_clf = imputer.fit_transform(X_clf)
y_clf = df['regime_label']
clf = RandomForestClassifier(random_state=42)
cv_scores = cross_val_score(clf, X_clf, y_clf, cv=5)
print("Regime Classifier CV Mean Accuracy:", cv_scores.mean())
clf.fit(X_clf, y_clf)
df['predicted_regime'] = clf.predict(X_clf)


# Generator Classifier
df['generator_label'] = df['otype_int']
y_gen = df['generator_label']
gen_clf = RandomForestClassifier(random_state=42)
cv_scores_gen = cross_val_score(gen_clf, X_clf, y_gen, cv=5)
print("Generator Classifier CV Mean Accuracy:", cv_scores_gen.mean())
gen_clf.fit(X_clf, y_gen)
df['predicted_type'] = gen_clf.predict(X_clf)


# Balance
smote = SMOTE(random_state=42)
X_res, y_res = smote.fit_resample(X_clf, y_clf)


# Regime split
df_gal = df[df['predicted_regime'] == 0]
df_clust = df[df['predicted_regime'] == 1]


# Models function
def run_models(X, y, regime):
    X = imputer.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    pysr_model = PySRRegressor(
        niterations=300,
        binary_operators=["+", "-", "*", "/", "pow"],
        unary_operators=["log", "exp", "sqrt", "sin", "cos"],
        extra_sympy_mappings={'inv': lambda x: 1/x},
        elementwise_loss="loss(prediction, target) = (prediction - target)^2",
        model_selection="best",
        complexity_of_operators={"pow": 3, "exp": 2, "log": 2, "sin": 2, "cos": 2},
        maxsize=30,
        maxdepth=6,
        parsimony=0.005,
        random_state=42,
        deterministic=True,
        parallelism='serial',
        constraints={'^': (-1, 1)}
    )
    pysr_model.fit(X_train_scaled, y_train)
    
    y_pred_pysr_train = pysr_model.predict(X_train_scaled).reshape(-1, 1)  # Fixed: Compute train/test separately
    y_pred_pysr = pysr_model.predict(X_test_scaled).reshape(-1, 1)
    r2_pysr = r2_score(y_test, y_pred_pysr)
    mae_pysr = mean_absolute_error(y_test, y_pred_pysr)
    
    xgb_model = XGBRegressor(n_estimators=200, learning_rate=0.03, max_depth=6, random_state=42, early_stopping_rounds=20)
    xgb_model.fit(X_train_scaled, y_train, eval_set=[(X_test_scaled, y_test)], verbose=False)
    
    y_pred_xgb_train = xgb_model.predict(X_train_scaled).reshape(-1, 1)
    y_pred_xgb = xgb_model.predict(X_test_scaled).reshape(-1, 1)
    r2_xgb = r2_score(y_test, y_pred_xgb)
    mae_xgb = mean_absolute_error(y_test, y_pred_xgb)
    
    # Non-linear stacking
    stack_train = np.hstack((X_train_scaled, y_pred_pysr_train, y_pred_xgb_train))
    stack_test = np.hstack((X_test_scaled, y_pred_pysr, y_pred_xgb))
    meta_model = XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=4, random_state=42)
    meta_model.fit(stack_train, y_train)
    y_pred_stack = meta_model.predict(stack_test)
    
    r2_stack = r2_score(y_test, y_pred_stack)
    mae_stack = mean_absolute_error(y_test, y_pred_stack)
    
    print(f"{regime} PySR R²: {r2_pysr:.4f}, MAE: {mae_pysr:.4f}")
    print(f"{regime} XGBoost R²: {r2_xgb:.4f}, MAE: {mae_xgb:.4f}")
    print(f"{regime} Stacked R²: {r2_stack:.4f}, MAE: {mae_stack:.4f}")
    
    return pysr_model, xgb_model, meta_model, X_test, y_pred_pysr, y_pred_xgb, y_pred_stack


# Run for regime
for regime, dfr in [('galactic', df_gal), ('cluster', df_clust)]:
    if len(dfr) < 2: continue
    Xr = dfr[X_clf_cols]
    yr = dfr['z']
    pysr_model, xgb_model, meta_model, X_test, y_pred_pysr, y_pred_xgb, y_pred_stack = run_models(Xr, yr, regime.capitalize())
    
    X_test_df = pd.DataFrame(X_test, columns=X_clf_cols)
    X_test_df['predicted_type'] = gen_clf.predict(X_test)
    
    # PNG Scatter (PySR)
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(X_test_df['flux_gr'], y_pred_pysr, c=X_test_df['EBV'], cmap='viridis')
    ax.set_title(f'{regime.capitalize()} PySR Projection')
    ax.set_xlabel('g/r Flux')
    ax.set_ylabel('Predicted z')
    fig.colorbar(scatter, label='EBV')
    fig.savefig(f"visualizations/{regime}_pysr_scatter.png")
    plt.close(fig)
    
    # HTML 3D (Stacked)
    fig = go.Figure(data=go.Scatter3d(
        x=X_test_df['flux_gr'], y=X_test_df['flux_rz'], z=y_pred_stack,
        mode='markers', marker=dict(size=5, color=y_pred_stack, colorscale='Viridis', showscale=True)
    ))
    fig.update_layout(title=f'{regime.capitalize()} Stacked Manifold')
    fig.write_html(f"visualizations/{regime}_stack_manifold_3d.html")
    
    # Type Binned 3D
    fig = go.Figure(data=go.Scatter3d(
        x=X_test_df['flux_gr'], y=X_test_df['flux_rz'], z=y_pred_stack,
        mode='markers', marker=dict(size=5, color=X_test_df['predicted_type'], colorscale='Viridis', showscale=True, colorbar_title='Generator Type')
    ))
    fig.update_layout(title=f'{regime.capitalize()} Stacked Manifold Binned by Type')
    fig.write_html(f"visualizations/{regime}_type_binned_3d.html")
