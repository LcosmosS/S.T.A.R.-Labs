# Run this in your notebook — it saves the latest colored point cloud
import pandas as pd
import numpy as np
import healpy as hp
from plyfile import PlyData, PlyElement

# Make sure df is loaded and has x/y/z + radiation
if 'df' not in globals():
    df = pd.read_csv("DESIDR8_SDSSDR16.csv")

# Use the same preprocessing as before (safe version)
nside = 64
ra_rad = np.deg2rad(df['RAdeg'].values)
dec_rad = np.deg2rad(df['DEdeg'].values)
pixel_indices = hp.ang2pix(nside, ra_rad, dec_rad, lonlat=True)
df['healpix_density'] = np.bincount(pixel_indices, minlength=hp.nside2npix(nside))[pixel_indices]

color = df['gmag'] - df['rmag']
df['local_conductor'] = np.nan_to_num(
    1.2 * np.log1p(df['healpix_density']) *
    (df['zphot'] ** 0.45) *
    np.exp(-9.0 * color.clip(-2, 3)),
    nan=0.0, posinf=20.0, neginf=0.0
)
df['cosmic_rank'] = np.clip(np.round(df['local_conductor'] * 2.1).astype(int), 0, 5)

dist = df['comoving_dc_Mpc'].values if 'comoving_dc_Mpc' in df.columns else np.ones(len(df)) * 1000
df['x'] = dist * np.cos(dec_rad) * np.cos(ra_rad)
df['y'] = dist * np.cos(dec_rad) * np.sin(ra_rad)
df['z'] = dist * np.sin(dec_rad)

# Radiation for coloring
df['radiation'] = np.exp(0.4 * df['cosmic_rank'])

# Export to Blender-friendly PLY
vertex = np.array(list(zip(df['x'], df['y'], df['z'], df['radiation'])),
                  dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4'), ('radiation', 'f4')])

ply_element = PlyElement.describe(vertex, 'vertex')
PlyData([ply_element]).write("cosmic_topography_radiation_blender.ply")

print("✅ Exported cosmic_topography_radiation_blender.ply — ready for Blender!")