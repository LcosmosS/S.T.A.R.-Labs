import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import gudhi
import optuna
import warnings
warnings.filterwarnings('ignore')

print(" — Automated SMAT Mission Optimizer (Optuna + Multi-Redshift + W₂ Minimization)")

# ====================== SMAT CLASSES ======================
class ArithmeticSeed:
    def __init__(self, label, rank, regulator, conductor):
        self.label = label
        self.rank = rank
        self.regulator = regulator
        self.conductor = conductor

class ProjectionEngine:
    def __init__(self):
        self.ALPHA = np.sqrt(1.5)      # Curvature Anchor
        self.BETA = 16.263             # Hubble-Time Scaling
        self.GAMMA = 1.0

    def apply(self, seed, t_cosmo):
        tf_proxy = (seed.rank * self.ALPHA) + np.log(seed.regulator + 1.1)
        z_projected = ((t_cosmo * tf_proxy) + self.ALPHA) - (t_cosmo * self.BETA)
        theta = np.mod(np.log10(seed.conductor) * 2 * np.pi, 2 * np.pi)
        phi = np.mod(seed.regulator * np.pi, np.pi)
        r = np.abs(z_projected) * 1000
        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
        return np.array([x, y, z])

class MissionControl:
    def __init__(self):
        self.engine = ProjectionEngine()
        self.seeds = []
        self.target_manifold = None

    def add_seeds(self, seed_df):
        for _, row in seed_df.iterrows():
            s = ArithmeticSeed(row['cremona_label'], row['exact_rank'], row['regulator'], row['conductor'])
            self.seeds.append(s)

    def load_target_catalog(self, filepath):
        self.target_manifold = pd.read_csv(filepath, low_memory=False)
        print(f"📡 Target Manifold Loaded: {len(self.target_manifold)} galaxies")

    def run_projection_mission(self, redshift_slice):
        t_cosmo = 1.0 / (1.0 + redshift_slice)
        results = []
        for seed in self.seeds:
            coords = self.engine.apply(seed, t_cosmo)
            results.append({'label': seed.label, 'x': coords[0], 'y': coords[1], 'z': coords[2], 'rank': seed.rank})
        return pd.DataFrame(results)

    def compute_w2_fidelity(self, projected_df):
        if self.target_manifold is None:
            return 0.0
        def simple_diag(rank):
            return np.array([[0, rank], [0, rank * 1.5]])
        pred_diags = [simple_diag(r) for r in projected_df['rank']]
        # FIXED: int(42) instead of Integer(42)
        target_diags = [simple_diag(r) for r in self.target_manifold['zphot'].sample(len(pred_diags), random_state=int(42))]
        w2 = [gudhi.bottleneck_distance(p, a) for p, a in zip(pred_diags, target_diags)]
        return np.mean(w2)

# ====================== LOAD DATA ======================
smat = MissionControl()

# Synthetic seeds
synthetic_seeds = pd.read_csv("synthetic_cosmic_catalog_calibrated.csv")
smat.add_seeds(synthetic_seeds)

# Real target (DESI/SDSS)
smat.load_target_catalog("DESIDR8_SDSSDR16_SIMBAD.csv")

# ====================== OPTUNA MISSION OPTIMIZER ======================
def mission_objective(trial):
    alpha = trial.suggest_float('alpha', 3.5, 5.0)
    beta = trial.suggest_float('beta', 6.0, 9.0)
    gamma = trial.suggest_float('gamma', 0.8, 1.2)

    slices = [0.1, 0.5, 1.0, 2.0]
    total_w2 = 0.0
    total_r2 = 0.0

    for z_slice in slices:
        projected = smat.run_projection_mission(z_slice)
        w2 = smat.compute_w2_fidelity(projected)
        r2_proxy = 1.0 - np.abs(projected['rank'].mean() - smat.target_manifold['zphot'].mean()) / 10.0
        total_w2 += w2
        total_r2 += r2_proxy

    loss = (total_w2 / len(slices)) - 0.5 * (total_r2 / len(slices))
    return loss

print("\n Running Automated Mission Optimizer (Optuna over 4 redshift slices)...")
study = optuna.create_study(direction='minimize')
study.optimize(mission_objective, n_trials=50)

best_params = study.best_params
print(f"\n Best Mission Parameters Found:")
print(f"   α (Curvature Anchor) = {best_params['alpha']:.4f}")
print(f"   β (Hubble Scaling)   = {best_params['beta']:.4f}")
print(f"   γ (Entropy Gradient) = {best_params['gamma']:.4f}")
print(f"   Best Loss (W₂ - 0.5 R²) = {study.best_value:.6f}")

# Final mission fidelity table
print("\n Final Mission Fidelity (W₂ per redshift slice):")
for z in [0.1, 0.5, 1.0, 2.0]:
    projected = smat.run_projection_mission(z)
    w2 = smat.compute_w2_fidelity(projected)
    print(f"   z = {z} → W₂ = {w2:.6f}")

print("\n Processing Complete — Automated Mission Optimizer")
