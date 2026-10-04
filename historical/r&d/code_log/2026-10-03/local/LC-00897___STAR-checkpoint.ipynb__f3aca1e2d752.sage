import pandas as pd
import numpy as np

print("🚀 Generating PLY files for Blender (20 frames of cosmic web expansion)")

# Load seeds
df_seeds = pd.read_csv("synthetic_cosmic_catalog_calibrated.csv")

class ProjectionEngine:
    def __init__(self):
        self.ALPHA = 3.7459
        self.BETA = 8.4532
        self.GAMMA = 1.0667

    def apply(self, rank, regulator, conductor, t_cosmo):
        tf_proxy = (rank * self.ALPHA) + np.log(regulator + 1.1)
        z_projected = ((t_cosmo * tf_proxy) + self.ALPHA) - (t_cosmo * self.BETA)
        theta = np.mod(np.log10(conductor) * 2 * np.pi, 2 * np.pi)
        phi = np.mod(regulator * np.pi, np.pi)
        r = np.abs(z_projected) * 1000
        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
        return x, y, z

engine = ProjectionEngine()

# 20 frames: z from 10.0 → 0.0
for frame in range(20):
    z = 10.0 * (1.0 - frame / 19.0)
    t_cosmo = 1.0 / (1.0 + z)
    
    vertices = []
    for _, row in df_seeds.iterrows():
        x, y, z_coord = engine.apply(row['exact_rank'], row['regulator'], row['conductor'], t_cosmo)
        # Color by rank (0-3 normalized to 0-255 for PLY)
        color = int(255 * row['exact_rank'] / 3)
        vertices.append((x, y, z_coord, color, 50, 255))  # R, G, B

    # Write PLY file
    filename = f"cosmic_web_frame_{frame:03d}.ply"
    with open(filename, "w") as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {len(vertices)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("end_header\n")
        for v in vertices:
            f.write(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f} {v[3]} {v[4]} {v[5]}\n")
    
    print(f"   Saved {filename} (z = {z:.2f})")

print("\n✅ All 20 PLY files generated!")
print("   Next: Open Blender and import them as a sequence.")