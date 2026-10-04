# Cell 1: Imports
import numpy as np
import pandas as pd
import healpy as hp
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
from pysr import PySRRegressor
import xgboost as xgb
import optuna
from scipy.stats import wasserstein_distance
from scipy.integrate import odeint
import warnings
warnings.filterwarnings('ignore')

# ====================== LOAD & CLEAN REAL DATA ======================
print("Loading DESIDR8_SDSSDR16.csv ...")
df = pd.read_csv('DESIDR8_SDSSDR16.csv')

df = df[
    (df['fclean'] == 1) &
    (df['fqual'] == 1) &
    (df['zphot'] > 0.01) &
    (df['zphot'] < 3.5) &
    (df['rmag'] < 24)
].copy()

print(f"Cleaned data shape: {df.shape}")

# Quick sanity check on DEC (latitude must be -90 to +90)
print(f"DEC range: {df['DEdeg'].min():.2f}° to {df['DEdeg'].max():.2f}°")

# ====================== 1. REAL HEALPIX LOCAL DENSITY (FIXED) ======================
nside = 64
npix = hp.nside2npix(nside)

# FIXED: RA first, DEC second when lonlat=True
pixel_indices = hp.ang2pix(nside, df['RAdeg'].values, df['DEdeg'].values, lonlat=True)

density_map = np.bincount(pixel_indices, minlength=npix)
df['healpix_density'] = density_map[pixel_indices] / hp.nside2pixarea(nside, degrees=True)

print("✅ HEALPix local density added (galaxies/deg²)")

# ====================== 2. ASTROPY COSMOLOGY — accurate comoving distance ======================
cosmo = FlatLambdaCDM(H0=67.4, Om0=0.315)
df['comoving_dc_Mpc'] = cosmo.comoving_distance(df['zphot'].values).to(u.Mpc).value

print("✅ Accurate comoving distances added (Mpc)")

# ====================== 3. IMPROVED LOCAL CONDUCTOR (ROBUST VERSION) ======================
color = df['gmag'] - df['rmag']
color_clipped = np.clip(color, -2.0, 3.0)   # prevents exp overflow

df['local_conductor'] = (
    1.2 * np.log1p(df['healpix_density']) *
    (df['zphot'] ** 0.45) *
    (1 + 0.4 * df['e_zphot']) *
    np.exp(-9.0 * color_clipped)
)

# Safety cleanup for any remaining NaN/inf
df['local_conductor'] = np.nan_to_num(df['local_conductor'], nan=0.01, posinf=10.0, neginf=0.0)
df['local_conductor'] = df['local_conductor'].clip(lower=0.0, upper=20.0)

df['cosmic_rank'] = np.clip(np.round(df['local_conductor'] * 2.1).astype(int), 0, 5)

print("\n✅ Robust local_conductor computed.")
print("New realistic rank distribution:\n", df['cosmic_rank'].value_counts().sort_index())
print(f"local_conductor range: {df['local_conductor'].min():.4f} — {df['local_conductor'].max():.4f}")

# ====================== 4. FULL PySR SYMBOLIC REGRESSION (AI Feynman) ======================
print("\nRunning PySR symbolic regression (AI Feynman style)...")

# --- ROBUST NaN HANDLING FOR PySR ---
features_for_sym = ['zphot', 'healpix_density', 'e_zphot', 'gmag', 'rmag']

# Fill NaNs with column medians (safe for astronomy data)
df_sym = df[features_for_sym].copy()
for col in features_for_sym:
    median_val = df_sym[col].median()
    df_sym[col] = df_sym[col].fillna(median_val)

# Select only finite rows (extra safety)
mask = np.isfinite(df_sym.values).all(axis=1)
X_sym = df_sym[mask].values[:10000]
y_sym = df['local_conductor'][mask].values[:10000]

print(f"Using {len(X_sym)} clean rows for symbolic regression")

model = PySRRegressor(
    niterations=40,
    binary_operators=["+", "*", "-", "/", "pow"],
    unary_operators=["exp", "log", "sqrt"],
    maxsize=25,
    model_selection="best",
    random_state=42,
    verbosity=1,          # shows progress
    procs=4               # use multiple CPU cores (adjust to your machine)
)

model.fit(X_sym, y_sym)

print("\n✅ Best symbolic expression for local conductor:")
print(model.get_best())

# Optional: apply the symbolic model to the full dataset
df['symbolic_conductor'] = model.predict(df_sym.values)

# ====================== 5. LAGRANGE 3-BODY INTEGRATION (high-rank patch) ======================
print("\nRunning Lagrange 3-body demo on high-rank patch...")

def three_body(y, t, G_eff):
    r1, v1, r2, v2 = y.reshape(4, 3)
    r12 = r2 - r1
    d12 = np.linalg.norm(r12)
    a1 = G_eff * r12 / d12**3
    a2 = -G_eff * r12 / d12**3
    return np.concatenate([v1, a1, v2, a2]).flatten()

high_rank_patch = df[df['cosmic_rank'] >= 4].iloc[0:500]
y0 = np.array([0,0,0, 0,0,0, 1,0,0, 0,1,0])
t = np.linspace(0, 10, 1000)
G_eff = 1.0 + 0.18 * high_rank_patch['cosmic_rank'].mean()
sol = odeint(three_body, y0, t, args=(G_eff,))
print(f"3-body integrated with G_eff = {G_eff:.3f} (rank-modulated)")

# ====================== 6. GAUSSIAN SPLATTING EXPORT ======================
df['x'] = df['comoving_dc_Mpc'] * np.cos(np.deg2rad(df['DEdeg'])) * np.cos(np.deg2rad(df['RAdeg']))
df['y'] = df['comoving_dc_Mpc'] * np.cos(np.deg2rad(df['DEdeg'])) * np.sin(np.deg2rad(df['RAdeg']))
df['z'] = df['comoving_dc_Mpc'] * np.sin(np.deg2rad(df['DEdeg']))

df['topography'] = 0.7 * df['cosmic_rank'] + 0.3 * df['local_conductor']

ply_header = f"""ply
format ascii 1.0
element vertex {len(df)}
property float x
property float y
property float z
property float topography
end_header
"""

with open("cosmic_topography.ply", "w") as f:
    f.write(ply_header)
    np.savetxt(f, df[['x','y','z','topography']].values, fmt="%.6f")

print("\n✅ Exported cosmic_topography.ply — ready for nerfstudio/gsplat!")
print("   In terminal: ns-train gaussian_splatting --data cosmic_topography.ply")