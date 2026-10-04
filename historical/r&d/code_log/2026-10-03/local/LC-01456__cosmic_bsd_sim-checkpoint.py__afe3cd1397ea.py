import pandas as pd
import numpy as np
from scipy.integrate import odeint
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from astropy.cosmology import FlatLambdaCDM
import healpy as hp

print("Loading DESIDR8_SDSSDR16.csv ...")
df = pd.read_csv("DESIDR8_SDSSDR16.csv")
print(f"Loaded {len(df):,} rows")

# ====================== ROBUST PREPROCESSING ======================
# HEALPix density
nside = 64
ra_rad = np.deg2rad(df['RAdeg'].values)
dec_rad = np.deg2rad(df['DEdeg'].values)
pixel_indices = hp.ang2pix(nside, ra_rad, dec_rad, lonlat=True)
df['healpix_density'] = np.bincount(pixel_indices, minlength=hp.nside2npix(nside))[pixel_indices]

# Comoving distance
cosmo = FlatLambdaCDM(H0=67.4, Om0=0.315)
df['comoving_dc_Mpc'] = cosmo.comoving_distance(df['zphot']).value

# Local conductor with full NaN/inf protection
color = df['gmag'] - df['rmag']
df['local_conductor'] = (
    1.2 * np.log1p(df['healpix_density']) *
    (df['zphot'] ** 0.45) *
    (1 + 0.4 * df.get('e_zphot', pd.Series(0, index=df.index))) *
    np.exp(-9.0 * color.clip(-2, 3))
)

# Safe conversion to cosmic_rank (this was the crashing line)
df['local_conductor'] = np.nan_to_num(df['local_conductor'], nan=0.0, posinf=20.0, neginf=0.0)
df['cosmic_rank'] = np.clip(np.round(df['local_conductor'] * 2.1).astype(int), 0, 5)

# Cartesian coordinates
dist = df['comoving_dc_Mpc'].values
df['x'] = dist * np.cos(dec_rad) * np.cos(ra_rad)
df['y'] = dist * np.cos(dec_rad) * np.sin(ra_rad)
df['z'] = dist * np.sin(dec_rad)

print("✅ Preprocessing complete")
print("Rank distribution:\n", df['cosmic_rank'].value_counts().sort_index())

# ====================== DASHBOARD ======================
sample = df.sample(15000, random_state=42).copy()

sample['metallicity'] = sample.get('Z', sample['gmag'] - sample['rmag'])
sample['radiation'] = np.exp(0.4 * sample['cosmic_rank'])

fig = make_subplots(
    rows=2, cols=2,
    specs=[[{"type": "scatter3d"}, {"type": "xy"}],
           [{"type": "xy", "colspan": 2}, None]],
    subplot_titles=("3D Cosmic Topography (Metallicity + Radiation)", 
                    "Full N-body Orbit (click any point)", 
                    "Cosmic L(s) at selected patch")
)

scatter = go.Scatter3d(
    x=sample['x'], y=sample['y'], z=sample['z'],
    mode='markers',
    marker=dict(size=2.5, color=sample['metallicity'], colorscale='Plasma', opacity=0.85),
    customdata=sample[['cosmic_rank', 'radiation', 'metallicity']],
    hovertemplate="Rank: %{customdata[0]}<br>Radiation: %{customdata[1]:.2f}<br>Metallicity: %{customdata[2]:.3f}<extra></extra>"
)
fig.add_trace(scatter, row=1, col=1)

# Full N-body
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

def update_on_click(trace, points, selector):
    if not points.point_inds: return
    idx = points.point_inds[0]
    local_rank = int(sample.iloc[idx]['cosmic_rank'])
    G_eff = 1.0 + 0.18 * local_rank
    
    np.random.seed(42)
    y0 = np.random.randn(10*6) * 0.5
    y0[3*10:] *= 0.1
    
    t = np.linspace(0, 60, 1000)
    sol = odeint(n_body, y0, t, args=(G_eff, 10))
    
    fig.data[1].x = sol[:, 0::6].flatten()
    fig.data[1].y = sol[:, 1::6].flatten()
    fig.data[1].marker.color = np.repeat(np.arange(10), len(t))
    
    fig.data[2].y = np.log(np.abs(np.sin(np.linspace(0.5, 1.5, 1000)) * (local_rank + 1)))
    
    fig.layout.title = f"Cosmic Rank {local_rank} | G_eff = {G_eff:.3f}"
    fig.update_layout(title_text=fig.layout.title)

fig.add_trace(go.Scatter(x=[], y=[], mode='lines+markers', name='N-body', marker=dict(size=3)), row=1, col=2)
fig.add_trace(go.Scatter(x=np.linspace(0.5,1.5,1000), y=np.zeros(1000), mode='lines', name='log L(s)'), row=2, col=1)

fig.data[0].on_click(update_on_click)

fig.update_layout(height=950, title="Cosmic BSD Simulator — Metallicity + Radiation + Full N-body")
fig.show()