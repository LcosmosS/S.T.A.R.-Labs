import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.integrate import odeint
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u

# ====================== 1. LOAD YOUR DATA ======================
print("Loading DESIDR8_SDSSDR16.csv ...")
df = pd.read_csv("DESIDR8_SDSSDR16.csv")

# ====================== 2. ROBUST COSMIC RANK CALCULATION ======================
def symbolic_conductor(zphot, gmag, rmag):
    x0 = zphot
    x3 = gmag
    x4 = rmag
    return (x0 / (0.091752805 * (x3 + 1.4800166 - x4))) - (4.0900064 * x0)

df['local_conductor'] = symbolic_conductor(df['zphot'], df['gmag'], df['rmag'])

# === CRITICAL FIX: remove NaN/inf before integer conversion ===
df['local_conductor'] = np.nan_to_num(df['local_conductor'], nan=0.0, posinf=20.0, neginf=0.0)
df['local_conductor'] = np.clip(df['local_conductor'], 0, 20)   # reasonable range

df['cosmic_rank'] = np.clip(np.round(df['local_conductor'] * 2.1).astype(int), 0, 5)

# ====================== 3. COMOVING DISTANCE & CARTESIAN COORDINATES ======================
cosmo = FlatLambdaCDM(H0=67.4, Om0=0.315)
df['comoving_dc_Mpc'] = cosmo.comoving_distance(df['zphot']).to(u.Mpc).value

ra_rad = np.deg2rad(df['RAdeg'])
dec_rad = np.deg2rad(df['DEdeg'])
df['x'] = df['comoving_dc_Mpc'] * np.cos(dec_rad) * np.cos(ra_rad)
df['y'] = df['comoving_dc_Mpc'] * np.cos(dec_rad) * np.sin(ra_rad)
df['z'] = df['comoving_dc_Mpc'] * np.sin(dec_rad)

# Metallicity & radiation layers
df['metallicity'] = df.get('Z', df['gmag'] - df['rmag'])
df['radiation'] = np.exp(0.4 * df['cosmic_rank'])

print(f"✅ Loaded {len(df):,} galaxies")
print("Rank distribution:\n", df['cosmic_rank'].value_counts().sort_index())

# ====================== 4. ALL-IN-ONE INTERACTIVE DASHBOARD ======================
sample = df.sample(15000, random_state=42).copy()

fig = make_subplots(
    rows=2, cols=3,
    specs=[[{"type": "scatter", "colspan": 2}, None, {"type": "scatter3d"}],
           [{"type": "xy", "colspan": 2}, None, {"type": "xy"}]],
    subplot_titles=("SDSS-like Sky Map (Cosmic Rank at s=1)", 
                    "3D Topography (Radiation + Metallicity)",
                    "Rank-modulated N-body Orbit (click any point)",
                    "Cosmic L(s) at selected patch")
)

# 1. SDSS-like sky map (aitoff projection)
ra_rad = np.deg2rad(sample['RAdeg'])
dec_rad = np.deg2rad(sample['DEdeg'])
x = 2 * np.sqrt(2) * np.cos(dec_rad) * np.sin(ra_rad/2) / np.sqrt(1 + np.cos(dec_rad) * np.cos(ra_rad/2))
y = np.sqrt(2) * np.sin(dec_rad) / np.sqrt(1 + np.cos(dec_rad) * np.cos(ra_rad/2))

sky = go.Scatter(
    x=x, y=y, mode='markers',
    marker=dict(size=3, color=sample['cosmic_rank'], colorscale='Plasma', opacity=0.9),
    customdata=sample[['cosmic_rank', 'radiation', 'metallicity']],
    hovertemplate="Rank: %{customdata[0]}<br>Radiation: %{customdata[1]:.2f}<br>Metallicity: %{customdata[2]:.3f}<extra></extra>",
    name="Sky Map"
)
fig.add_trace(sky, row=1, col=1)

# 2. 3D topography
topo = go.Scatter3d(
    x=sample['x'], y=sample['y'], z=sample['z'],
    mode='markers',
    marker=dict(size=2, color=sample['metallicity'], colorscale='Plasma', opacity=0.85),
    customdata=sample[['cosmic_rank', 'radiation', 'metallicity']],
    hovertemplate="Rank: %{customdata[0]}<br>Radiation: %{customdata[1]:.2f}<br>Metallicity: %{customdata[2]:.3f}<extra></extra>",
    name="3D Topography"
)
fig.add_trace(topo, row=1, col=3)

# 3. Empty N-body trace
fig.add_trace(go.Scatter(x=[], y=[], mode='lines+markers', marker=dict(size=4), name='N-body'), row=2, col=1)

# 4. L(s) trace
fig.add_trace(go.Scatter(x=np.linspace(0.5,1.5,800), y=np.zeros(800), mode='lines', name='log L(s)'), row=2, col=3)

# N-body function
def n_body(y, t, G_eff, n_bodies=10):
    pos = y[:3*n_bodies].reshape((n_bodies, 3))
    vel = y[3*n_bodies:].reshape((n_bodies, 3))
    acc = np.zeros_like(pos)
    for i in range(n_bodies):
        for j in range(n_bodies):
            if i == j: continue
            r = pos[j] - pos[i]
            dist = np.linalg.norm(r) + 1e-6
            acc[i] += G_eff * r / dist**3
    return np.concatenate([vel.flatten(), acc.flatten()])

def on_click(trace, points, selector):
    if not points.point_inds: return
    idx = points.point_inds[0]
    local_rank = int(sample.iloc[idx]['cosmic_rank'])
    G_eff = 1.0 + 0.18 * local_rank
    
    np.random.seed(42)
    y0 = np.random.randn(10*6) * 0.5
    y0[3*10:] *= 0.1
    t = np.linspace(0, 60, 1000)
    sol = odeint(n_body, y0, t, args=(G_eff, 10))
    
    fig.data[2].x = sol[:, 0::6].flatten()
    fig.data[2].y = sol[:, 1::6].flatten()
    fig.data[2].marker.color = np.repeat(np.arange(10), len(t))
    
    fig.data[3].y = np.log(np.abs(np.sin(np.linspace(0.5,1.5,800)) * (local_rank + 1) + 0.1))
    
    fig.layout.title = f"Cosmic Rank {local_rank} | G_eff = {G_eff:.3f} | N-body active"
    fig.update_layout(title_text=fig.layout.title)

# Connect clicks to both maps
fig.data[0].on_click(on_click)   # sky map
fig.data[1].on_click(on_click)   # 3D map

fig.update_layout(height=1100, title="All-in-One Cosmic BSD Simulator — SDSS-like Sky Map + 3D Topography + N-body + L(s)")
fig.show()