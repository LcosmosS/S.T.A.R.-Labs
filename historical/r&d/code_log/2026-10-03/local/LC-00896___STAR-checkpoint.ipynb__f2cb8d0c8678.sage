import pandas as pd
import numpy as np

class ArithmeticSeed:
    def __init__(self, label, rank, regulator, conductor):
        self.label = label
        self.rank = rank
        self.regulator = regulator
        self.conductor = conductor

class ProjectionEngine:
    def __init__(self):
        self.ALPHA = 3.7459
        self.BETA = 8.4532
        self.GAMMA = 1.0667

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

# Load seeds
df_seeds = pd.read_csv("synthetic_cosmic_catalog_calibrated.csv")
seeds = []
for _, row in df_seeds.iterrows():
    seeds.append(ArithmeticSeed(row['cremona_label'], row['exact_rank'], row['regulator'], row['conductor']))

engine = ProjectionEngine()

frames = []
for frame, z in enumerate(np.linspace(10.0, 0.0, 20)):   # 20 frames: early → present
    t_cosmo = 1.0 / (1.0 + z)
    for seed in seeds:
        coords = engine.apply(seed, t_cosmo)
        frames.append({
            'frame': frame,
            'z': z,
            't_cosmo': t_cosmo,
            'label': seed.label,
            'rank': seed.rank,
            'x': coords[0],
            'y': coords[1],
            'z_coord': coords[2]
        })

pd.DataFrame(frames).to_csv("cosmic_web_expansion.csv", index=False)
print("✅ cosmic_web_expansion.csv generated (20 frames, ready for Blender)")