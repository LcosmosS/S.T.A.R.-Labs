import pandas as pd
import numpy as np
from plyfile import PlyData, PlyElement

print("Loading DESIDR8_SDSSDR16_SIMBAD.csv ...")
df = pd.read_csv("DESIDR8_SDSSDR16_SIMBAD.csv", low_memory=False)

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

# ====================== COMOVING DISTANCE + CARTESIAN ======================
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
cosmo = FlatLambdaCDM(H0=67.4, Om0=0.315)
df['comoving_dc_Mpc'] = cosmo.comoving_distance(df['zphot']).to(u.Mpc).value

ra_rad = np.deg2rad(df['RAdeg'])
dec_rad = np.deg2rad(df['DEdeg'])
df['x'] = df['comoving_dc_Mpc'] * np.cos(dec_rad) * np.cos(ra_rad)
df['y'] = df['comoving_dc_Mpc'] * np.cos(dec_rad) * np.sin(ra_rad)
df['z'] = df['comoving_dc_Mpc'] * np.sin(dec_rad)

# ====================== CLEAN METALLICITY + RADIATION ======================
df['metallicity'] = df.get('Z', df['gmag'] - df['rmag'])
df['metallicity'] = np.nan_to_num(df['metallicity'], nan=0.0, posinf=1.0, neginf=-1.0)
df['metallicity'] = np.clip(df['metallicity'], -1.0, 2.0)   # reasonable range

df['radiation'] = np.exp(0.4 * df['cosmic_rank'])
df['radiation'] = np.nan_to_num(df['radiation'], nan=0.0, posinf=100.0, neginf=0.0)

print(f"✅ Loaded {len(df):,} galaxies | Rank distribution:\n{df['cosmic_rank'].value_counts().sort_index()}")

# ====================== SAFE PLY EXPORT ======================
print("Exporting cosmic_full_enhanced.ply ...")

vertex_data = np.zeros(len(df), dtype=[
    ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
    ('red', 'u1'), ('green', 'u1'), ('blue', 'u1'),
    ('cosmic_rank', 'u1'),
    ('radiation', 'f4'),
    ('metallicity', 'f4')
])

vertex_data['x'] = df['x']
vertex_data['y'] = df['y']
vertex_data['z'] = df['z']
vertex_data['red']   = (df['radiation'] * 255).clip(0, 255).astype(np.uint8)
vertex_data['green'] = ((df['metallicity'] + 1.0) * 127).clip(0, 255).astype(np.uint8)
vertex_data['blue']  = (df['cosmic_rank'] * 51).clip(0, 255).astype(np.uint8)
vertex_data['cosmic_rank'] = df['cosmic_rank']
vertex_data['radiation'] = df['radiation']
vertex_data['metallicity'] = df['metallicity']

vertex_element = PlyElement.describe(vertex_data, 'vertex')
PlyData([vertex_element]).write("cosmic_full_enhanced.ply")

print(f"✅ Successfully exported cosmic_full_enhanced.ply ({len(df):,} points)")
print("   → Ready for Blender + Gaussian Splatting")