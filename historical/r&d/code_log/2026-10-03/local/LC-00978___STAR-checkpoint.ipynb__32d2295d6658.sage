import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

# 1. LOAD AND CLEAN
file_path = "JApJ94494_2MASS_GAIADR3_EPOCH.csv"
df = pd.read_csv(file_path, low_memory=False)

# Use the columns detected in your previous run
ra_col, dec_col, vel_col, mag_col = 'RAJ2000', 'DEJ2000', 'Vcmb', 'Gmag'

# FORCE NATIVE TYPES: This strips SageMath wrappers to prevent the ValueError
df = df.dropna(subset=[ra_col, dec_col, vel_col]).copy()
df_native = pd.DataFrame({
    'ra': df[ra_col].values.astype(float),
    'dec': df[dec_col].values.astype(float),
    'vel': df[vel_col].values.astype(float),
    'mag': df[mag_col].fillna(df[mag_col].mean()).values.astype(float)
})

# 2. CALCULATE STRUCTURAL RANK (Cosmic Web Topology)
print("🧮 Analyzing 3D clustering density for structural legends...")
H0 = 70.0 # Standard Hubble proxy
dist_mpc = df_native['vel'] / H0

# Convert RA/Dec/Dist to Cartesian (X, Y, Z in Mpc)
ra_rad = np.deg2rad(df_native['ra'])
dec_rad = np.deg2rad(df_native['dec'])
coords_3d = np.column_stack([
    dist_mpc * np.cos(dec_rad) * np.cos(ra_rad),
    dist_mpc * np.cos(dec_rad) * np.sin(ra_rad),
    dist_mpc * np.sin(dec_rad)
])

# Find 10 nearest neighbors to determine if an object is in a Void or Cluster
nbrs = NearestNeighbors(n_neighbors=11).fit(coords_3d)
distances, _ = nbrs.kneighbors(coords_3d)
avg_neighbor_dist = distances[:, 1:].mean(axis=1) # Average distance to neighbors

# Structural Density Proxy (Higher = Denser)
density = 1.0 / (avg_neighbor_dist + 1e-6)

# Manually create Bins to avoid Sage/Pandas qcut conflict
bins = np.percentile(density, [0, 25, 50, 75, 100])
df_native['rank'] = (np.digitize(density, np.unique(bins), right=True) - 1).clip(0, 3)

# 3. EXPORT 4D REPLICA
def export_real_replica(df_n, scale_val=0.01):
    frames = []
    num_frames = 25 # Number of animation steps
    
    print(f"🚀 Rendering {num_frames} frames of 1/100th scale universe...")
    
    # Pre-calculated expansion vectors
    base_r = (df_n['vel'] / 70.0) * scale_val
    ra_rad = np.deg2rad(df_n['ra'])
    dec_rad = np.deg2rad(df_n['dec'])
    
    # Normalize Gravity and Radiation for Blender (0.0 to 1.0)
    grav = (1.0 / (df_n['mag'] + 1)).rank(pct=True)
    rad = df_n['rank'] / 3.0 # Radiation proxy tied to structural density

    for frame in range(num_frames):
        # T_cosmo goes from 0.1 (Early Expansion) to 1.0 (Today)
        t_cosmo = 0.1 + (frame / (num_frames - 1)) * 0.9
        r_t = base_r * t_cosmo
        
        frame_data = pd.DataFrame({
            'frame': int(frame),
            'x': r_t * np.cos(dec_rad) * np.cos(ra_rad),
            'y': r_t * np.cos(dec_rad) * np.sin(ra_rad),
            'z': r_t * np.sin(dec_rad),
            'rank': df_n['rank'].astype(int),
            'gravity': grav,
            'radiation': rad
        })
        frames.append(frame_data)
        if frame % 5 == 0: print(f"   Frame {frame} written...")

    pd.concat(frames).to_csv("real_cosmic_web_replica_v2.csv", index=False)
    print("📡 SUCCESS: 'real_cosmic_web_replica_v2.csv' ready for Blender.")

export_real_replica(df_native)