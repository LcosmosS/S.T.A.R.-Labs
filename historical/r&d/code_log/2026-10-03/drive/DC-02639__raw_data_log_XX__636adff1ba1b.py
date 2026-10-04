import numpy as np
import pandas as pd
from sage.all import *
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from gplearn.genetic import SymbolicRegressor
from optuna import create_study
import warnings
warnings.filterwarnings("ignore")


# ————————————————————————
# 1. S.T.A.R. INVERSE b → ρ + SCALING
# ————————————————————————
def inverse_b_to_rho(b, mass, v_disp, r_mpc):
    log_mass = np.log10(mass)
    return round(b / (2.0 * log_mass * v_disp / r_mpc))


def star_scale_rho(rho, R=3.383, Omega=0.422, T=1, rank=3):
    Psi_r = rank * (rank + 1) / 2
    scale = (Omega * T**2 * np.exp(Psi_r / Omega)) / R
    return rho * (scale**rank) * np.exp(-1 / Omega)


# ————————————————————————
# 2. GENERATOR DICHOTOMY CLASSIFIER
# ————————————————————————
def classify_generator_type(P_actual):
    """Simple: integer coords | Recursive: 3-power denominators"""
    if P_actual is None:
        return None
    x, y, z = P_actual
    x, y = x/z, y/z
    # Check if denominators are powers of 3
    den_x = x.denominator()
    den_y = y.denominator()
    is_power_of_3 = lambda d: d > 1 and all(f == 3 for f, _ in factor(d))
    return "Recursive" if is_power_of_3(den_x) and is_power_of_3(den_y) else "Simple"


# ————————————————————————
# 3. DATA PREPARATION
# ————————————————————————
def prepare_data(clusters):
    data = []
    for name, r, b, mass, v_disp, r_mpc in clusters:
        try:
            # Inverse b → ρ
            rho = inverse_b_to_rho(b, mass, v_disp, r_mpc)
            rho_star = star_scale_rho(rho)
            
            # Derive curve
            a = -round(31.59259 * r)
            E = EllipticCurve(QQ, [a, b])
            E.two_descent(second_limit=20, verbose=False)
            rank = E.rank(only_use_mwrank=False)
            gens = E.gens()
            P = gens[0] if rank > 0 else None
            
            # Dichotomy
            gen_type = classify_generator_type(P)
            if gen_type is None: continue
            
            # Extract numerators/denominators
            if P:
                x, y, z = P
                x, y = x/z, y/z
                num_x, den_x = x.numerator(), x.denominator()
                num_y, den_y = y.numerator(), y.denominator()
            else:
                num_x = num_y = den_x = den_y = np.nan
            
            data.append({
                "name": name,
                "r": r, "rho": rho, "rho_star": rho_star,
                "a": a, "b": b, "rank": rank,
                "gen_type": gen_type,
                "num_x": float(num_x), "num_y": float(num_y),
                "den_x": float(den_x), "den_y": float(den_y)
            })
        except:
            continue
    return pd.DataFrame(data)


# ————————————————————————
# 4. ML PIPELINE
# ————————————————————————
def run_ml_pipeline(df):
    # Features
    X = df[["r", "rho_star", "rank"]].values
    y_type = df["gen_type"].map({"Simple": 0, "Recursive": 1}).values
    
    # Split
    X_train, X_test, y_train_type, y_test_type = train_test_split(
        X, y_type, test_size=0.3, random_state=42, stratify=y_type
    )
    
    # ——— CLASSIFIER: Predict Dichotomy ———
    clf = XGBRegressor(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train_type)
    type_pred = (clf.predict(X_test) > 0.5).astype(int)
    acc = np.mean(type_pred == y_test_type)
    print(f"Dichotomy Accuracy: {acc:.3f}")
    
    # ——— REGRESSOR: Predict num_x, num_y (Recursive only) ———
    rec_idx = df["gen_type"] == "Recursive"
    X_rec = df[rec_idx][["r", "rho_star", "rank"]].values
    y_num_x = df[rec_idx]["num_x"].values
    y_num_y = df[rec_idx]["num_y"].values
    
    if len(X_rec) > 3:
        Xr_train, Xr_test, yx_train, yx_test, yy_train, yy_test = train_test_split(
            X_rec, y_num_x, y_num_y, test_size=0.3, random_state=42
        )
        
        # Gradient Boosters
        models = {
            "XGB": XGBRegressor(n_estimators=200),
            "LGBM": LGBMRegressor(n_estimators=200),
            "CatBoost": CatBoostRegressor(verbose=0, iterations=200)
        }
        
        best_r2 = -1
        best_model = None
        for name, model in models.items():
            model.fit(Xr_train, np.column_stack([yx_train, yy_train]))
            pred = model.predict(Xr_test)
            r2 = r2_score(np.column_stack([yx_test, yy_test]), pred)
            print(f"{name} R²: {r2:.3f}")
            if r2 > best_r2:
                best_r2 = r2
                best_model = model
        
        # ——— SYMBOLIC REGRESSION: Discover Sequence ———
        est = SymbolicRegressor(
            population_size=5000, generations=20,
            function_set=('add', 'sub', 'mul', 'div', 'log', 'sqrt'),
            metric='mse', parsimony_coefficient=0.01
        )
        est.fit(Xr_train, yx_train)
        print(f"Symbolic num_x: {est._program}")
        
        est.fit(Xr_train, yy_train)
        print(f"Symbolic num_y: {est._program}")
    
    return clf, best_model, acc


# ————————————————————————
# 5. RUN PIPELINE
# ————————————————————————
clusters = [
    ("Virgo", 54, 6200, 1.5e15, 750, 2.2),
    ("Coma", 321, 9980, 2.0e15, 978, 3.0),
