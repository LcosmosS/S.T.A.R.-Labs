import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.integrate import odeint
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u

# ====================== LOAD YOUR DATA ======================
print("Loading DESIDR8_SDSSDR16_SIMBAD.csv ...")
df = pd.read_csv("DESIDR8_SDSSDR16_SIMBAD.csv")

# ====================== ROBUST COSMIC RANK ======================
def symbolic_conductor(zphot, gmag, rmag):
    x0 = zphot
    x3 = gmag
    x4 = rmag
    return (x0 / (0.091752805 * (x3 + 1.4800166 - x4))) - (4.0900064 * x0)

df['local_conductor'] = symbolic_conductor(df['zphot'], df['gmag'], df['rmag'])
df['local_conductor'] = np.nan_to_num(df['local_conductor'], nan=0.0, posinf=20.0, neginf=0.0)
df['local_conductor'] = np.clip(df['local_conductor'], 0, 20)
df['cosmic_rank'] = np.clip(np.round(df['local_conductor'] * 2.1).astype(int), 0, 5)

# Comoving distance + Cartesian coordinates
cosmo = FlatLambdaCDM(H0=67.4, Om0=0.315)
df['comoving_dc_Mpc'] = cosmo.comoving_distance(df['zphot']).to(u.Mpc).value

ra_rad = np.deg2rad(df['RAdeg'])
dec_rad = np.deg2rad(df['DEdeg'])
df['x'] = df['comoving_dc_Mpc'] * np.cos(dec_rad) * np.cos(ra_rad)
df['y'] = df['comoving_dc_Mpc'] * np.cos(dec_rad) * np.sin(ra_rad)
df['z'] = df['comoving_dc_Mpc'] * np.sin(dec_rad)

df['metallicity'] = df.get('Z', df['gmag'] - df['rmag'])
df['radiation'] = np.exp(0.4 * df['cosmic_rank'])

print(f"✅ Loaded {len(df):,} galaxies | Rank distribution:\n{df['cosmic_rank'].value_counts().sort_index()}")

# ====================== ALL-IN-ONE DASHBOARD ======================
sample = df.sample(18000, random_state=42).copy()

fig = make_subplots(
    rows=2, cols=3,
    specs=[[{"type": "scatter3d", "colspan": 2}, None, {"type": "scatter3d"}],
           [{"type": "xy", "colspan": 2}, None, {"type": "xy"}]],
    subplot_titles=("3D Celestial Sky Map (Cosmic Rank at s=1)", 
                    "3D Topography (Radiation + Metallicity)",
                    "20-Body N-body Orbit (click any point)",
                    "Cosmic L(s) at selected patch")
)

# Cosmic theme settings
cosmic_layout = dict(
    scene=dict(
        xaxis=dict(backgroundcolor="black", gridcolor="rgba(100,180,255,0.15)", zerolinecolor="rgba(100,180,255,0.3)"),
        yaxis=dict(backgroundcolor="black", gridcolor="rgba(100,180,255,0.15)", zerolinecolor="rgba(100,180,255,0.3)"),
        zaxis=dict(backgroundcolor="black", gridcolor="rgba(100,180,255,0.15)", zerolinecolor="rgba(100,180,255,0.3)"),
        bgcolor="black"
    ),
    paper_bgcolor="black",
    plot_bgcolor="black",
    font_color="white"
)

# 1. 3D Celestial Sky Map (fully rotatable)
r = 1.0
theta = np.pi/2 - np.deg2rad(sample['DEdeg'])
phi = np.deg2rad(sample['RAdeg'])
x_sky = r * np.sin(theta) * np.cos(phi)
y_sky = r * np.sin(theta) * np.sin(phi)
z_sky = r * np.cos(theta)

sky3d = go.Scatter3d(
    x=x_sky, y=y_sky, z=z_sky,
    mode='markers',
    marker=dict(size=3, color=sample['cosmic_rank'], colorscale='Plasma', opacity=0.9),
    customdata=sample[['cosmic_rank', 'radiation', 'metallicity']],
    hovertemplate="Rank: %{customdata[0]}<br>Radiation: %{customdata[1]:.2f}<br>Metallicity: %{customdata[2]:.3f}<extra></extra>",
    name="Sky Map"
)
fig.add_trace(sky3d, row=1, col=1)

# 2. 3D Topography
topo = go.Scatter3d(
    x=sample['x'], y=sample['y'], z=sample['z'],
    mode='markers',
    marker=dict(size=2, color=sample['metallicity'], colorscale='Plasma', opacity=0.85),
    customdata=sample[['cosmic_rank', 'radiation', 'metallicity']],
    hovertemplate="Rank: %{customdata[0]}<br>Radiation: %{customdata[1]:.2f}<br>Metallicity: %{customdata[2]:.3f}<extra></extra>",
    name="3D Topography"
)
fig.add_trace(topo, row=1, col=3)

# 3. N-body trace
fig.add_trace(go.Scatter(x=[], y=[], mode='lines+markers', marker=dict(size=4), name='N-body'), row=2, col=1)

# 4. L(s) trace
fig.add_trace(go.Scatter(x=np.linspace(0.5,1.5,800), y=np.zeros(800), mode='lines', name='log L(s)'), row=2, col=3)

# 20-body N-body function
def n_body(y, t, G_eff, n_bodies=20):
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
    y0 = np.random.randn(20*6) * 0.5
    y0[3*20:] *= 0.1
    t = np.linspace(0, 60, 1200)
    sol = odeint(n_body, y0, t, args=(G_eff, 20))
    
    fig.data[2].x = sol[:, 0::6].flatten()
    fig.data[2].y = sol[:, 1::6].flatten()
    fig.data[2].marker.color = np.repeat(np.arange(20), len(t))
    
    fig.data[3].y = np.log(np.abs(np.sin(np.linspace(0.5,1.5,800)) * (local_rank + 1) + 0.1))
    
    fig.layout.title = f"Cosmic Rank {local_rank} | G_eff = {G_eff:.3f} | 20-body active"
    fig.update_layout(title_text=fig.layout.title)

# Connect clicks to BOTH 3D maps
fig.data[0].on_click(on_click)
fig.data[1].on_click(on_click)

fig.update_layout(
    height=1100,
    title="All-in-One Cosmic BSD Simulator — Rotatable 3D Sky + 3D Topography + 20-body N-body + L(s)",
    **cosmic_layout
)

fig.show()