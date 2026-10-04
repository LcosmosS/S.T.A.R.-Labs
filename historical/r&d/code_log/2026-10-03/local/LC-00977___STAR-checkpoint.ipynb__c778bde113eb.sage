import pandas as pd
import numpy as np

# 1. LOAD THE DATA
# We must load the synthetic seeds before we can process them.
try:
    synth = pd.read_csv("synthetic_cosmic_catalog_calibrated.csv")
    print(f"✅ Loaded {len(synth)} seeds. Preparing for 4D projection...")
except FileNotFoundError:
    print("⚠️ Could not find 'synthetic_cosmic_catalog_calibrated.csv'.")
    print("Creating a small test batch to verify the engine...")
    synth = pd.DataFrame({
        'cremona_label': ['11a1', '37a1', '53a1'],
        'exact_rank': [0, 1, 1],
        'regulator': [1.0, 0.198, 0.256],
        'conductor': [11, 37, 53]
    })

# 2. DEFINE THE ENGINE
def export_4d_telemetry(seeds, alpha=4.133, beta=7.436, scale_factor=0.01):
    """Generates time-series data for Blender at 1/100th scale."""
    frames = []
    
    print("🚀 Initiating 4D Telemetry generation (100 frames)...")
    
    # Loop through cosmic time (from T_cosmo = 0.1 to 1.0)
    for frame, t_cosmo in enumerate(np.linspace(0.1, 1.0, 100)):
        
        # Print progress every 25 frames so you know it's working
        if frame % 25 == 0:
            print(f"   -> Rendering Frame {frame} (T_cosmo = {t_cosmo:.2f})...")
            
        tf_proxy = (seeds['exact_rank'] * alpha) + np.log(seeds['regulator'] + 1.1)
        z_proj = ((t_cosmo * tf_proxy) + alpha) - (t_cosmo * beta)
        
        r = np.abs(z_proj) * 1000 * scale_factor # 1/100th scale applied here
        theta = np.mod(np.log10(seeds['conductor']) * 2 * np.pi, 2 * np.pi)
        phi = np.mod(seeds['regulator'] * np.pi, np.pi)
        
        frame_data = seeds.copy()
        frame_data['frame'] = frame
        frame_data['x'] = r * np.sin(phi) * np.cos(theta)
        frame_data['y'] = r * np.sin(phi) * np.sin(theta)
        frame_data['z'] = r * np.cos(phi)
        
        # Normalize Gravity and Radiation between 0.0 and 1.0 for Blender Shaders
        max_reg = seeds['regulator'].max() if seeds['regulator'].max() > 0 else 1
        max_cond = np.log10(seeds['conductor'].max()) if seeds['conductor'].max() > 1 else 1
        
        frame_data['gravity'] = seeds['regulator'] / max_reg
        frame_data['radiation'] = np.log10(seeds['conductor']) / max_cond
        
        frames.append(frame_data)
        
    final_4d_data = pd.concat(frames)
    final_4d_data.to_csv("smat_blender_telemetry.csv", index=False)
    print(f"📡 SUCCESS: 4D Telemetry Exported. ({len(final_4d_data)} total data points written to 'smat_blender_telemetry.csv')")

# 3. EXECUTE THE ENGINE (Uncommented!)
export_4d_telemetry(synth, alpha=4.133, beta=7.436, scale_factor=0.01)