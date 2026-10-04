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