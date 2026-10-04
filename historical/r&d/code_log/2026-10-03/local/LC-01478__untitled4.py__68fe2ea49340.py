import pandas as pd
import numpy as np
from plyfile import PlyData, PlyElement
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.cosmology import FlatLambdaCDM

# Load file
df = pd.read_csv("DESIDR8_SDSSDR16_SIMBAD.csv", low_memory=False)

# Existing cosmic rank + coordinates 
def symbolic_conductor(zphot, gmag, rmag):
    x0 = zphot; x3 = gmag; x4 = rmag
    return (x0 / (0.091752805 * (x3 + 1.4800166 - x4))) - (4.0900064 * x0)

df['local_conductor'] = symbolic_conductor(df['zphot'], df['gmag'], df['rmag'])
df['local_conductor'] = np.nan_to_num(df['local_conductor'], nan=0.0, posinf=20.0, neginf=0.0)
df['local_conductor'] = np.clip(df['local_conductor'], 0, 20)
df['cosmic_rank'] = np.clip(np.round(df['local_conductor'] * 2.1).astype(int), 0, 5)

cosmo = FlatLambdaCDM(H0=67.4, Om0=0.315)
df['comoving_dc_Mpc'] = cosmo.comoving_distance(df['zphot']).to(u.Mpc).value
ra_rad = np.deg2rad(df['RAdeg'])
dec_rad = np.deg2rad(df['DEdeg'])
df['x'] = df['comoving_dc_Mpc'] * np.cos(dec_rad) * np.cos(ra_rad)
df['y'] = df['comoving_dc_Mpc'] * np.cos(dec_rad) * np.sin(ra_rad)
df['z'] = df['comoving_dc_Mpc'] * np.sin(dec_rad)

df['metallicity'] = df.get('Z', df['gmag'] - df['rmag'])
df['metallicity'] = np.nan_to_num(df['metallicity'], nan=0.0, posinf=2.0, neginf=-1.0)
df['radiation'] = np.exp(0.4 * df['cosmic_rank'])

print(f"✅ Cosmic data ready ({len(df):,} galaxies)")

# ====================== HELIOCENTRIC SOLAR SYSTEM (Sun at origin) ======================
print("Adding heliocentric Solar System...")

with solar_system_ephemeris.set('builtin'):
    t = Time('2025-01-01')
    bodies = ['sun','mercury','venus','earth','mars','jupiter','saturn','uranus','neptune']
    solar_data = []
    for name in bodies:
        pos = get_body_barycentric(name, t)
        solar_data.append({
            'name': name.capitalize(),
            'x': pos.x.to(u.au).value,
            'y': pos.y.to(u.au).value,
            'z': pos.z.to(u.au).value,
            'cosmic_rank': 5 if name == 'sun' else 3,
            'metallicity': 0.0 if name == 'sun' else -0.2,
            'radiation': 100 if name == 'sun' else 10
        })

solar_df = pd.DataFrame(solar_data)

# Scale AU to match cosmic Mpc scale (1 AU ≈ 1.58e-5 Mpc, we scale for visibility)
au_to_mpc_scale = 1e-4 * 1e6   # adjust this number to make Solar System bigger/smaller
solar_df[['x','y','z']] *= au_to_mpc_scale

print(f"   → Added {len(solar_df)} Solar System bodies")

# ====================== ADD FAMOUS OBJECTS (heliocentric + cosmic scale) ======================
famous = pd.DataFrame({
    'name': ['Sun', 'Earth', 'Betelgeuse', 'Sirius', 'Andromeda Galaxy', 'M87 (Virgo)', 'Sagittarius A*', 'Orion Nebula', 'Virgo Cluster'],
    'ra_deg':  [0, 0, 88.79, 101.29, 10.68, 187.71, 266.42, 83.82, 186.0],
    'dec_deg': [0, 0, 7.41, -16.72, 41.27, 12.39, -29.01, -5.39, 12.5],
    'distance_mpc': [0, 0, 0.000197, 0.0000086, 0.778, 16.4, 0.008, 0.000414, 16.5],
    'cosmic_rank': [5, 3, 4, 2, 4, 5, 5, 3, 5],
    'radiation': [100, 15, 45, 20, 30, 80, 90, 25, 70],
    'metallicity': [0.0, 0.0, -0.1, 0.2, -0.3, -0.2, -0.4, 0.1, -0.25]
})

# Convert to Cartesian (same scale as your galaxies)
cosmo = FlatLambdaCDM(H0=67.4, Om0=0.315)
famous['comoving_dc_Mpc'] = famous['distance_mpc']
ra_rad = np.deg2rad(famous['ra_deg'])
dec_rad = np.deg2rad(famous['dec_deg'])
famous['x'] = famous['comoving_dc_Mpc'] * np.cos(dec_rad) * np.cos(ra_rad)
famous['y'] = famous['comoving_dc_Mpc'] * np.cos(dec_rad) * np.sin(ra_rad)
famous['z'] = famous['comoving_dc_Mpc'] * np.sin(dec_rad)

# Merge with main data
full_df = pd.concat([df, famous], ignore_index=True)

# ====================== FINAL PLY WITH LABELS ======================
vertex_data = np.zeros(len(full_df), dtype=[
    ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
    ('red', 'u1'), ('green', 'u1'), ('blue', 'u1'),
    ('cosmic_rank', 'u1'), ('radiation', 'f4'), ('metallicity', 'f4')
])

vertex_data['x'] = full_df['x']
vertex_data['y'] = full_df['y']
vertex_data['z'] = full_df['z']
vertex_data['red']   = (full_df['radiation'] * 255).clip(0, 255).astype(np.uint8)
vertex_data['green'] = ((full_df['metallicity'] + 1.0) * 127).clip(0, 255).astype(np.uint8)
vertex_data['blue']  = (full_df['cosmic_rank'] * 51).clip(0, 255).astype(np.uint8)
vertex_data['cosmic_rank'] = full_df['cosmic_rank']
vertex_data['radiation'] = full_df['radiation']
vertex_data['metallicity'] = full_df['metallicity']

vertex_element = PlyElement.describe(vertex_data, 'vertex')
PlyData([vertex_element]).write("cosmic_heliocentric_labeled.ply")

print("✅ Exported cosmic_heliocentric_labeled.ply with Solar System + famous objects")
print("   Sun is at origin. Ready for Blender.")