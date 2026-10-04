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
import warnings
warnings.filterwarnings('ignore')

print("Loading DESIDR8_SDSSDR16.csv ...")
df = pd.read_csv('DESIDR8_SDSSDR16.csv')

df = df[(df['fclean'] == 1) & (df['fqual'] == 1) & 
        (df['zphot'] > 0.01) & (df['zphot'] < 3.5) & (df['rmag'] < 24)].copy()

print(f"Cleaned data shape: {df.shape}")

# HEALPix local density
nside = 64
pixel_indices = hp.ang2pix(nside, df['RAdeg'].values, df['DEdeg'].values, lonlat=True)
density_map = np.bincount(pixel_indices, minlength=hp.nside2npix(nside))
df['healpix_density'] = density_map[pixel_indices] / hp.nside2pixarea(nside, degrees=True)

# Accurate comoving distance
cosmo = FlatLambdaCDM(H0=67.4, Om0=0.315)
df['comoving_dc_Mpc'] = cosmo.comoving_distance(df['zphot'].values).to(u.Mpc).value

# NEW BEST SYMBOLIC CONDUCTOR FROM PySR REFINEMENT
def symbolic_conductor(zphot, gmag, rmag):
    x0 = zphot
    x3 = gmag
    x4 = rmag
    return (x0 / (0.091752805 * (x3 + 1.4800166 - x4))) - (4.0900064 * x0)

df['local_conductor'] = symbolic_conductor(df['zphot'], df['gmag'], df['rmag'])
df['local_conductor'] = np.nan_to_num(df['local_conductor'], nan=0.01, posinf=10.0, neginf=0.0)
df['local_conductor'] = df['local_conductor'].clip(0.0, 20.0)

df['cosmic_rank'] = np.clip(np.round(df['local_conductor'] * 2.1).astype(int), 0, 5)

print("\nRank distribution:\n", df['cosmic_rank'].value_counts().sort_index())
df['pixel'] = pixel_indices

print("Computing cosmic L-function and analytic rank map at s=1...")

pixel_stats = df.groupby('pixel').agg({
    'local_conductor': 'mean',
    'zphot': 'mean',
    'cosmic_rank': 'mean'
}).reset_index()

s = 1.0
Q = 1 + pixel_stats['zphot']
local_euler = 1 - pixel_stats['local_conductor'] * (Q ** -s)
pixel_stats['log_L_contrib'] = -np.log(np.clip(local_euler, 1e-8, None))

ds = 0.001
L_plus = -np.log(np.clip(1 - pixel_stats['local_conductor'] * (Q ** -(s+ds)), 1e-8, None))
L_minus = -np.log(np.clip(1 - pixel_stats['local_conductor'] * (Q ** -(s-ds)), 1e-8, None))
pixel_stats['analytic_rank'] = np.abs(L_plus - L_minus) / (2 * ds)

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
hp.mollview(rank_map, title="Cosmic Analytic Rank at s=1", cmap="viridis", unit="rank proxy")
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

print("✅ cosmic_topography.ply exported — load into nerfstudio/gsplat")

# Interactive 3-body Lagrange orbits (modulated by cosmic rank)
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
    if len(data1) < 50 or len(data2) < 50:   # raised threshold
        result.value = f"Pixel {pixel1.value} or {pixel2.value} has too few galaxies"
    else:
        cost = wasserstein_distance(data1, data2)
        result.value = f"Interstellar travel/comms cost (Wasserstein-2): {cost:.4f}"

print("Exporting enhanced Gaussian splat with radiation coloring...")

# Radiation intensity (exponential boost from cosmic rank)
df['radiation'] = np.exp(0.4 * df['cosmic_rank'])

df['x'] = df['comoving_dc_Mpc'] * np.cos(np.deg2rad(df['DEdeg'])) * np.cos(np.deg2rad(df['RAdeg']))
df['y'] = df['comoving_dc_Mpc'] * np.cos(np.deg2rad(df['DEdeg'])) * np.sin(np.deg2rad(df['RAdeg']))
df['z'] = df['comoving_dc_Mpc'] * np.sin(np.deg2rad(df['DEdeg']))

df['topography'] = 0.7 * df['cosmic_rank'] + 0.3 * df['local_conductor']

# Enhanced .ply with radiation color
ply_header = f"""ply
format ascii 1.0
element vertex {len(df)}
property float x
property float y
property float z
property float topography
property float radiation
end_header
"""

with open("cosmic_topography_radiation.ply", "w") as f:
    f.write(ply_header)
    np.savetxt(f, df[['x','y','z','topography','radiation']].values, fmt="%.6f")

print("✅ cosmic_topography_radiation.ply exported (with radiation layer)")
print("   Load in nerfstudio: ns-train gaussian_splatting --data cosmic_topography_radiation.ply")

import plotly.graph_objects as go
from plotly.subplots import make_subplots

print("Launching interactive cosmic dashboard...")

# Subsample for smooth Plotly rendering (you can increase)
sample = df.sample(8000, random_state=42)

fig = make_subplots(
    rows=2, cols=2,
    specs=[[{"type": "scatter3d", "colspan": 2}, None],
           [{"type": "scatter"}, {"type": "scatter"}]],
    subplot_titles=("3D Cosmic Topography Map (click a point for 3-body orbit)",
                    "Rank-modulated 3-body Lagrange Orbit",
                    "Cosmic L(s) Function at selected patch")
)

# 3D splat with radiation coloring
scatter3d = go.Scatter3d(
    x=sample['x'], y=sample['y'], z=sample['z'],
    mode='markers',
    marker=dict(
        size=2,
        color=sample['radiation'],
        colorscale='Plasma',
        opacity=0.8,
        colorbar=dict(title="Radiation Intensity")
    ),
    name="Cosmic Map",
    hovertemplate="Rank: %{customdata[0]}<br>Topography: %{customdata[1]:.2f}<br>Radiation: %{customdata[2]:.2f}<extra></extra>",
    customdata=np.stack((sample['cosmic_rank'], sample['topography'], sample['radiation']), axis=1)
)

fig.add_trace(scatter3d, row=1, col=1)

# 3-body orbit placeholder (will update on click)
orbit_trace = go.Scatter(x=[], y=[], mode='lines', name='Body 1', line=dict(color='blue'))
fig.add_trace(orbit_trace, row=2, col=1)

# L(s) curve placeholder
ls_trace = go.Scatter(x=[], y=[], mode='lines', name='log L(s)', line=dict(color='red'))
fig.add_trace(ls_trace, row=2, col=2)

fig.update_layout(
    height=900,
    title="Cosmic BSD Simulator — Interactive 3-body + Radiation + L(s)",
    scene=dict(xaxis_title="x (Mpc)", yaxis_title="y (Mpc)", zaxis_title="z (Mpc)"),
    showlegend=True
)

# Click handler for 3-body animation
def update_orbit(trace, points, selector):
    if not points.point_inds:
        return
    idx = points.point_inds[0]
    rank = sample.iloc[idx]['cosmic_rank']
    
    # Compute 3-body orbit
    def three_body(y, t, G_eff):
        r1, v1, r2, v2 = y.reshape(4, 3)
        r12 = r2 - r1
        d12 = np.linalg.norm(r12)
        a1 = G_eff * r12 / d12**3
        a2 = -G_eff * r12 / d12**3
        return np.concatenate([v1, a1, v2, a2]).flatten()
    
    G_eff = 1.0 + 0.18 * rank
    y0 = np.array([0.,0.,0., 0.,0.,0., 1.,0.,0., 0.,1.,0.])
    t = np.linspace(0, 20, 800)
    sol = odeint(three_body, y0, t, args=(G_eff,))
    
    with fig.batch_update():
        fig.data[1].x = sol[:,0]
        fig.data[1].y = sol[:,1]
        fig.layout.annotations[1].text = f"Rank-modulated 3-body (G_eff = {G_eff:.3f})"

scatter3d.on_click(update_orbit)

display(fig)

from matplotlib.animation import FuncAnimation
from io import BytesIO
import base64

print("Creating animated cosmic L(s) function...")

def symbolic_f(z):
    # Your latest refined conductor (mean values for demo)
    return 6.006567 / np.clip((0.00024169777 ** (20.5 - 19.8)) - ((19.8 - 20.5) / (0.49327 + np.sqrt(z))), 1e-8, None)

s_values = np.linspace(0.5, 1.5, 200)
fig_anim, ax = plt.subplots(figsize=(8,5))
line, = ax.plot([], [], lw=3, color='red')
ax.set_xlabel("s")
ax.set_ylabel("log L(s)")
ax.set_title("Cosmic L-function evolution around s=1")
ax.grid(True)

def animate(i):
    s = s_values[i]
    Q = 1 + df['zphot'].values[:5000]  # subsample
    L = -np.log(np.clip(1 - symbolic_f(df['zphot'].values[:5000]) * (Q ** -s), 1e-8, None))
    line.set_data(s_values[:i+1], np.mean(L) * np.ones(i+1))  # mean behaviour
    ax.set_xlim(0.5, 1.5)
    ax.set_ylim(-5, 20)
    return line,

ani = FuncAnimation(fig_anim, animate, frames=len(s_values), interval=30, blit=True)

# Save as GIF
ani.save("cosmic_Ls_animation.gif", writer='pillow', fps=30)
print("✅ cosmic_Ls_animation.gif saved — open it in any browser/image viewer")