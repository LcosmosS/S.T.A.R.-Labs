import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from gplearn.genetic import SymbolicRegressor
import warnings
from numpy.polynomial import Polynomial
from scipy.spatial import cKDTree


warnings.filterwarnings("ignore")


# Load dataset
df = pd.read_csv("merged_data.csv")


# Drop rows with missing target or excessive NaNs
df = df.dropna(subset=["log_SFR_Ha"])
df = df.dropna(axis=0, thresh=int(0.8 * df.shape[1]))
df.fillna(df.median(numeric_only=True), inplace=True)


# Load VizieR V/154 data (SDSS DR16 spectroscopic data)
sdss_data = pd.read_csv("sdss_dr16_spec.csv")  # Update with actual path


# Cross-match based on coordinates
def deg_to_rad(df, ra_col, dec_col):
    df['ra_rad'] = np.radians(df[ra_col])
    df['dec_rad'] = np.radians(df[dec_col])
    return df


df = deg_to_rad(df, 'objra_y', 'objdec')
sdss_data = deg_to_rad(sdss_data, 'RA', 'Dec')


coords1 = np.array([df['ra_rad'], df['dec_rad']]).T
coords2 = np.array([sdss_data['ra_rad'], sdss_data['dec_rad']]).T
tree = cKDTree(coords2)
max_dist = np.radians(1.0 / 3600.0)  # 1 arcsec
dist, idx = tree.query(coords1, k=1, distance_upper_bound=max_dist)
matched = dist < max_dist
df_matched = df[matched].copy()
sdss_matched = sdss_data.iloc[idx[matched]].copy()
df_matched = df_matched.reset_index(drop=True)
sdss_matched = sdss_matched.reset_index(drop=True)
df = pd.concat([df_matched, sdss_matched[['specz', 'flux_Ha', 'flux_Hb', 'flux_OIII_5007', 'flux_NII_6584', 'e_flux_Ha']]], axis=1)
print(f"Number of galaxies after cross-match: {len(df)}")


# Recompute log_SFR_Ha and metallicity from raw fluxes
df['Ha_Hb_observed'] = df['flux_Ha'] / df['flux_Hb']
Ha_Hb_intrinsic = 2.86
k_Ha = 2.468
k_Hb = 3.634
df['A_Ha'] = 2.5 * np.log10(df['Ha_Hb_observed'] / Ha_Hb_intrinsic) * (k_Ha / (k_Hb - k_Ha))
df['flux_Ha_corr'] = df['flux_Ha'] * 10**(0.4 * df['A_Ha'])
H0 = 70  # km/s/Mpc
c = 3e5  # km/s
df['DL'] = (c * df['specz'] / H0) * 3.0856e24  # cm
df['L_Ha'] = df['flux_Ha_corr'] * 4 * np.pi * df['DL']**2  # erg/s
df['log_SFR_Ha_raw'] = np.log10(df['L_Ha'] * 7.9e-42)  # M_sun/yr
df['log_O3N2_raw'] = np.log10((df['flux_OIII_5007'] / df['flux_Hb']) / (df['flux_NII_6584'] / df['flux_Ha']))
df['OH_O3N2_raw'] = 8.533 - 0.214 * df['log_O3N2_raw']


# Add raw fluxes as features
df['log_flux_Ha'] = np.log10(df['flux_Ha'] + 1e-10)
df['log_flux_Hb'] = np.log10(df['flux_Hb'] + 1e-10)
df['log_flux_OIII_5007'] = np.log10(df['flux_OIII_5007'] + 1e-10)
df['log_flux_NII_6584'] = np.log10(df['flux_NII_6584'] + 1e-10)
df['log_e_flux_Ha'] = np.log10(df['e_flux_Ha'] + 1e-10)


# Step 1: Cosmo-Rank Construction
gz_df = df.copy()
morph_cols = ['P(CD)', 'P(E)', 'P(S0)', 'P(Sa)', 'P(Sab)', 'P(Sb)', 'P(Sbc)', 
              'P(Sc)', 'P(Scd)', 'P(Sd)', 'P(Sdm)', 'P(Sm)', 'P(Irr)']
gz_df['morph_sum'] = gz_df[morph_cols].sum(axis=1)
gz_df['Num_w'] = gz_df['conf_prob']
scaler_rank = MinMaxScaler()
