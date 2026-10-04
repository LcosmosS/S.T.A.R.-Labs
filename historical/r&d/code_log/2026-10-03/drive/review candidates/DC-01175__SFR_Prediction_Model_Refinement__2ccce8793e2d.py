import pandas as pd
from qflac import QFLaC


# === Load the Pipe3D CSV ===
csv_path = 'pipe3d_data.csv'
q = QFLaC.from_csv(csv_path)


# === Set up cleaning parameters ===
q.clean(
    drop_nan_thresh=0.3,       # Remove columns with >30% NaNs
    snr_column='Ha_Hb_Re',     # Proxy for emission line S/N
    snr_min=3,                 # Minimum acceptable S/N
    clip_outliers=True,        # Automatically clip extreme outliers
    normalize=False            # Don’t normalize yet; your model will do that
)


# === Define features & target for your SFR model ===
core_features = [
    'log_Mass_gas',      # Gas mass (log scale)
    'OH_O3N2_cen',       # Metallicity indicator
    'Av_gas_Re',         # Dust attenuation (Re-weighted)
]


target = 'log_SFR_Ha'     # Star formation rate (from H-alpha)


# === Get clean modeling DataFrame ===
df_model = q.df_clean


# === Drop rows with NaNs in key columns ===
df_model = df_model[core_features + [target]].dropna()


# === Save to new CSV for modeling ===
df_model.to_csv('cleaned_pipe3d_sfr_model.csv', index=False)
print("✅ Cleaned data saved to: cleaned_pipe3d_sfr_model.csv")
