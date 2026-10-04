import pandas as pd
import numpy as np

# Reuse your SMAT classes (ProjectionEngine + seeds)
class ArithmeticSeed:
    def __init__(self, label, rank, regulator, conductor):
        self.label = label
        self.rank = rank
        self.regulator = regulator
        self.conductor = conductor

class ProjectionEngine:
    def __init__(self):
        self.ALPHA = np.sqrt(1.5)  # Curvature Anchor
        self.BETA = 16.263         # Hubble-Time Scaling
    def apply(self, seed, t_cosmo):
        tf_proxy = (seed.rank * self.ALPHA) + np.log(seed.regulator + 1.1)
        z_projected = ((t_cosmo * tf_proxy) + self.ALPHA) - (t_cosmo * self.BETA)
        theta = np.mod(np.log10(seed.conductor) * 2 * np.pi, 2 * np.pi)
        phi = np.mod(seed.regulator * np.pi, np.pi)
        r = np.abs(z_projected) * 1000
        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
        return np.array([x, y, z])

# Load your seeds
seed_df = pd.read_csv("synthetic_cosmic_catalog_calibrated.csv")
seeds = [ArithmeticSeed(row['cremona_label'], row['exact_rank'], row['regulator'], row['conductor']) for _, row in seed_df.iterrows()]

engine = ProjectionEngine()

# Generate frames at multiple redshift slices (time steps)
redshift_slices = [10.0, 5.0, 2.0, 1.0, 0.5, 0.1, 0.01]  # from early universe to today
for i, z in enumerate(redshift_slices):
    t_cosmo = 1.0 / (1.0 + z)
    frame_data = []
    for seed in seeds:
        coords = engine.apply(seed, t_cosmo)
        frame_data.append({
            'frame': i,
            'z_slice': z,
            't_cosmo': t_cosmo,
            'x': coords[0],
            'y': coords[1],
            'z': coords[2],
            'rank': seed.rank,
            'density': np.abs(coords[2])  # proxy for local density
        })
    df = pd.DataFrame(frame_data)
    df.to_csv(f"smat_projection_frame_{i:03d}_z{z:.2f}.csv", index=False)
    print(f"✅ Exported frame {i} (z={z}) → smat_projection_frame_{i:03d}_z{z:.2f}.csv")

print("\n🎉 All projection frames exported. Ready for Blender.")