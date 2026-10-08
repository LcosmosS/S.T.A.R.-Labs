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

# ====================== 3. FULL COSMIC L-FUNCTION + HEALPIX RANK MAP ======================
print("Computing cosmic L-function using symbolic conductor...")

# Exact symbolic conductor from PySR (best equation)
def symbolic_conductor(zphot, gmag, rmag):
    x0 = zphot
    x3 = gmag
    x4 = rmag
    denom = (0.00024169777 ** (x4 - x3)) - ((x3 - x4) / (0.49327 + np.sqrt(x0)))
    return 6.006567 / denom

# Compute per-galaxy conductor
df['symbolic_f'] = symbolic_conductor(df['zphot'], df['gmag'], df['rmag'])

# Group by HEALPix pixel
pixel_indices = hp.ang2pix(64, df['RAdeg'].values, df['DEdeg'].values, lonlat=True)
df['pixel'] = pixel_indices

# Per-pixel aggregates
pixel_stats = df.groupby('pixel').agg({
    'symbolic_f': 'mean',
    'zphot': 'mean',
    'cosmic_rank': 'mean'
}).reset_index()

# Cosmic L-function contribution at s=1 (local Euler factor)
s = 1.0
Q = 1 + pixel_stats['zphot']
local_euler = 1 - pixel_stats['symbolic_f'] * (Q ** -s)
pixel_stats['log_L_contrib'] = -np.log(np.clip(local_euler, 1e-8, None))   # safe log

# Proxy analytic rank at s=1 (finite-difference order of vanishing)
# For simplicity we use a smoothed derivative test (higher |dL/ds| near s=1 → higher rank)
ds = 0.001
L_plus = -np.log(np.clip(1 - pixel_stats['symbolic_f'] * (Q ** -(s+ds)), 1e-8, None))
L_minus = -np.log(np.clip(1 - pixel_stats['symbolic_f'] * (Q ** -(s-ds)), 1e-8, None))
pixel_stats['analytic_rank_proxy'] = np.abs(L_plus - L_minus) / (2 * ds)   # first derivative magnitude

# Create HEALPix map
nside = 64
rank_map = np.zeros(hp.nside2npix(nside))
logL_map = np.zeros(hp.nside2npix(nside))

for _, row in pixel_stats.iterrows():
    p = int(row['pixel'])
    rank_map[p] = row['analytic_rank_proxy']
    logL_map[p] = row['log_L_contrib']

# Save maps
hp.write_map("cosmic_analytic_rank_map.fits", rank_map, overwrite=True)
hp.write_map("cosmic_logL_map.fits", logL_map, overwrite=True)

print("✅ HEALPix maps saved:")
print("   cosmic_analytic_rank_map.fits   ← analytic rank proxy at s=1")
print("   cosmic_logL_map.fits            ← log L(s=1) contribution")

# Quick visualisation
hp.mollview(rank_map, title="Cosmic Analytic Rank Proxy at s=1 (HEALPix)", cmap="viridis", unit="rank proxy")
hp.graticule()
plt.show()

import ipywidgets as widgets
from IPython.display import display, clear_output
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# ====================== INTERACTIVE 3-BODY LAGRANGE ORBITS ======================
def plot_3body(rank_value):
    def three_body(y, t, G_eff):
        r1, v1, r2, v2 = y.reshape(4, 3)
        r12 = r2 - r1
        d12 = np.linalg.norm(r12)
        a1 = G_eff * r12 / d12**3
        a2 = -G_eff * r12 / d12**3
        return np.concatenate([v1, a1, v2, a2]).flatten()
    
    G_eff = 1.0 + 0.18 * rank_value
    y0 = np.array([0,0,0, 0,0,0, 1.0,0,0, 0,1.0,0])
    t = np.linspace(0, 20, 2000)
    sol = odeint(three_body, y0, t, args=(G_eff,))
    
    fig, ax = plt.subplots(figsize=(6,6))
    ax.plot(sol[:,0], sol[:,1], label="Body 1", lw=2)
    ax.plot(sol[:,3], sol[:,4], label="Body 2", lw=2)
    ax.set_title(f"Rank-modulated 3-body (G_eff = {G_eff:.3f})")
    ax.set_xlabel("x (AU)")
    ax.set_ylabel("y (AU)")
    ax.legend()
    ax.grid(True)
    plt.show()

# Widget: select cosmic rank
rank_slider = widgets.IntSlider(value=3, min=0, max=5, description='Cosmic Rank:')
out = widgets.Output()

def on_rank_change(change):
    with out:
        clear_output(wait=True)
        plot_3body(change['new'])

rank_slider.observe(on_rank_change, names='value')
display(rank_slider, out)
plot_3body(3)  # initial plot

# ====================== REAL-TIME WASSERSTEIN NAVIGATION ======================
def compute_wasserstein(pixel1, pixel2):
    data1 = df[df['pixel'] == pixel1]['zphot'].values
    data2 = df[df['pixel'] == pixel2]['zphot'].values
    if len(data1) < 10 or len(data2) < 10:
        return "Not enough galaxies in one pixel"
    return wasserstein_distance(data1, data2)

# Simple interactive selector (replace pixel numbers with your own from the map)
pixel1_input = widgets.IntText(value=100, description='Pixel 1:')
pixel2_input = widgets.IntText(value=200, description='Pixel 2:')
button = widgets.Button(description="Compute Interstellar Cost")
result_label = widgets.Label()

def on_button_click(b):
    cost = compute_wasserstein(pixel1_input.value, pixel2_input.value)
    result_label.value = f"Wasserstein-2 distance (travel/comms cost): {cost:.4f}"

button.on_click(on_button_click)
display(pixel1_input, pixel2_input, button, result_label)

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