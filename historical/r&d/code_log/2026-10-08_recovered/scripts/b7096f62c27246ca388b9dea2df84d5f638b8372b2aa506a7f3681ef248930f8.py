import numpy as np
import pandas as pd
import healpy as hp
import matplotlib.pyplot as plt
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
from scipy.integrate import odeint
from scipy.stats import wasserstein_distance
import ipywidgets as widgets
from IPython.display import display, clear_output
from pysr import PySRRegressor
import warnings
warnings.filterwarnings('ignore')

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
print(f"DEC range: {df['DEdeg'].min():.2f}° to {df['DEdeg'].max():.2f}°")

# HEALPix local density
nside = 64
pixel_indices = hp.ang2pix(nside, df['RAdeg'].values, df['DEdeg'].values, lonlat=True)
density_map = np.bincount(pixel_indices, minlength=hp.nside2npix(nside))
df['healpix_density'] = density_map[pixel_indices] / hp.nside2pixarea(nside, degrees=True)

# Accurate comoving distance
cosmo = FlatLambdaCDM(H0=67.4, Om0=0.315)
df['comoving_dc_Mpc'] = cosmo.comoving_distance(df['zphot'].values).to(u.Mpc).value

# EXACT PySR symbolic conductor
def symbolic_conductor(zphot, gmag, rmag):
    x0 = zphot
    x3 = gmag
    x4 = rmag
    denom = (0.00024169777 ** (x4 - x3)) - ((x3 - x4) / (0.49327 + np.sqrt(x0)))
    return 6.006567 / np.clip(denom, 1e-8, None)

df['local_conductor'] = symbolic_conductor(df['zphot'], df['gmag'], df['rmag'])
df['local_conductor'] = np.nan_to_num(df['local_conductor'], nan=0.01, posinf=10.0, neginf=0.0)
df['local_conductor'] = df['local_conductor'].clip(0.0, 20.0)

df['cosmic_rank'] = np.clip(np.round(df['local_conductor'] * 2.1).astype(int), 0, 5)

print("\nRank distribution:\n", df['cosmic_rank'].value_counts().sort_index())

print("Computing full cosmic L-function and analytic rank map at s=1...")

df['pixel'] = pixel_indices
pixel_stats = df.groupby('pixel').agg({
    'local_conductor': 'mean',
    'zphot': 'mean',
    'cosmic_rank': 'mean'
}).reset_index()

s = 1.0
Q = 1 + pixel_stats['zphot']
local_euler = 1 - pixel_stats['local_conductor'] * (Q ** -s)
pixel_stats['log_L_contrib'] = -np.log(np.clip(local_euler, 1e-8, None))

# Analytic rank proxy (finite-difference order of vanishing)
ds = 0.001
L_plus = -np.log(np.clip(1 - pixel_stats['local_conductor'] * (Q ** -(s+ds)), 1e-8, None))
L_minus = -np.log(np.clip(1 - pixel_stats['local_conductor'] * (Q ** -(s-ds)), 1e-8, None))
pixel_stats['analytic_rank'] = np.abs(L_plus - L_minus) / (2 * ds)

# Build HEALPix maps
npix = hp.nside2npix(nside)
rank_map = np.zeros(npix)
logL_map = np.zeros(npix)
for _, row in pixel_stats.iterrows():
    p = int(row['pixel'])
    rank_map[p] = row['analytic_rank']
    logL_map[p] = row['log_L_contrib']

hp.write_map("cosmic_analytic_rank_map.fits", rank_map, overwrite=True)
hp.write_map("cosmic_logL_map.fits", logL_map, overwrite=True)

print("✅ Saved cosmic_analytic_rank_map.fits and cosmic_logL_map.fits")
hp.mollview(rank_map, title="Cosmic Analytic Rank at s=1 (HEALPix nside=64)", cmap="viridis", unit="rank proxy")
hp.graticule()
plt.show()

print("Exporting Gaussian splat point cloud...")

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

print("✅ cosmic_topography.ply exported")
print("   Run: ns-train gaussian_splatting --data cosmic_topography.ply")

# Interactive 3-body Lagrange orbits
def plot_3body(rank_value):
    def three_body(y, t, G_eff):
        r1, v1, r2, v2 = y.reshape(4, 3)
        r12 = r2 - r1
        d12 = np.linalg.norm(r12)
        a1 = G_eff * r12 / d12**3
        a2 = -G_eff * r12 / d12**3
        return np.concatenate([v1, a1, v2, a2]).flatten()
    
    G_eff = 1.0 + 0.18 * rank_value
    y0 = np.array([0.,0.,0., 0.,0.,0., 1.,0.,0., 0.,1.,0.])
    t = np.linspace(0, 20, 2000)
    sol = odeint(three_body, y0, t, args=(G_eff,))
    
    fig, ax = plt.subplots(figsize=(6,6))
    ax.plot(sol[:,0], sol[:,1], label="Body 1", lw=2)
    ax.plot(sol[:,3], sol[:,4], label="Body 2", lw=2)
    ax.set_title(f"Rank-modulated 3-body orbit (G_eff = {G_eff:.3f})")
    ax.set_xlabel("x (AU)"); ax.set_ylabel("y (AU)")
    ax.legend(); ax.grid(True)
    plt.show()

rank_slider = widgets.IntSlider(value=3, min=0, max=5, description='Cosmic Rank:')
out = widgets.Output()
def on_change(change):
    with out: clear_output(wait=True); plot_3body(change['new'])
rank_slider.observe(on_change, names='value')
display(rank_slider, out)
plot_3body(3)

# Real-time Wasserstein navigation
pixel1 = widgets.IntText(value=100, description='Pixel 1:')
pixel2 = widgets.IntText(value=200, description='Pixel 2:')
btn = widgets.Button(description="Compute Travel Cost")
result = widgets.Label()

def on_click(b):
    data1 = df[df['pixel'] == pixel1.value]['zphot'].values
    data2 = df[df['pixel'] == pixel2.value]['zphot'].values
    if len(data1) < 10 or len(data2) < 10:
        result.value = "Not enough galaxies in one pixel"
    else:
        cost = wasserstein_distance(data1, data2)
        result.value = f"Interstellar cost (Wasserstein-2): {cost:.4f}"
btn.on_click(on_click)
display(pixel1, pixel2, btn, result)

# Optional refinement (run only if you want a stronger equation)
print("Refining PySR on larger sample...")
X_refine = df[['zphot','healpix_density','e_zphot','gmag','rmag']].fillna(0).values[:20000]
y_refine = df['local_conductor'].values[:20000]

refined_model = PySRRegressor(niterations=80, maxsize=30, procs=4, random_state=42)
refined_model.fit(X_refine, y_refine)
print("New best symbolic conductor:")
print(refined_model.get_best())