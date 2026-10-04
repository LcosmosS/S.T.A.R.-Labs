import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from gplearn.genetic import SymbolicRegressor
import optuna
import warnings
from numpy.polynomial import Polynomial
from scipy.spatial import cKDTree


warnings.filterwarnings("ignore")


# Load the original dataset
df = pd.read_csv("merged_data.csv")


# Load VizieR data (update paths as needed)
sdss_spec = pd.read_csv("sdss_dr16_spec.csv")  # V/154: Spectroscopic data
sdss_photo = pd.read_csv("sdss_dr12_photo.csv")  # V/147: Photometric data
twomass = pd.read_csv("2mass_xsc.csv")  # II/246: 2MASS Extended Source Catalogue
gama = pd.read_csv("gama_dr3.csv")  # II/356: GAMA DR3


# Cross-match function
def deg_to_rad(df, ra_col, dec_col):
    df['ra_rad'] = np.radians(df[ra_col])
    df['dec_rad'] = np.radians(df[dec_col])
    return df


def cross_match(df1, df2, ra_col1, dec_col1, ra_col2, dec_col2, max_dist_arcsec=1.0):
    df1 = deg_to_rad(df1, ra_col1, dec_col1)
    df2 = deg_to_rad(df2, ra_col2, dec_col2)
    coords1 = np.array([df1['ra_rad'], df1['dec_rad']]).T
    coords2 = np.array([df2['ra_rad'], df2['dec_rad']]).T
    tree = cKDTree(coords2)
    max_dist = np.radians(max_dist_arcsec / 3600.0)
    dist, idx = tree.query(coords1, k=1, distance_upper_bound=max_dist)
    matched = dist < max_dist
    df1_matched = df1[matched].copy()
    df2_matched = df2.iloc[idx[matched]].copy()
    df1_matched = df1_matched.reset_index(drop=True)
    df2_matched = df2_matched.reset_index(drop=True)
    return df1_matched, df2_matched


# Cross-match with VizieR catalogues
# V/154: SDSS DR16 spectroscopic data
df, sdss_spec_matched = cross_match(df, sdss_spec, 'objra_y', 'objdec', 'RA', 'Dec')
df = pd.concat([df, sdss_spec_matched[['specz', 'flux_Ha', 'flux_Hb', 'flux_OIII_5007', 'flux_NII_6584', 'e_flux_Ha']]], axis=1)
print(f"After V/154 cross-match: {len(df)} galaxies")


# V/147: SDSS DR12 photometric data
df, sdss_photo_matched = cross_match(df, sdss_photo, 'objra_y', 'objdec', 'RA', 'Dec')
df = pd.concat([df, sdss_photo_matched[['petroMag_u', 'petroMag_g', 'petroMag_r', 'petroMag_i', 'petroMag_z', 'petroMagErr_u', 'petroMagErr_g', 'petroMagErr_r', 'petroMagErr_i', 'petroMagErr_z']]], axis=1)
print(f"After V/147 cross-match: {len(df)} galaxies")


# II/246: 2MASS Extended Source Catalogue
df, twomass_matched = cross_match(df, twomass, 'objra_y', 'objdec', 'RA', 'Dec')
df = pd.concat([df, twomass_matched[['Jmag', 'Hmag', 'Kmag', 'e_Jmag', 'e_Hmag', 'e_Kmag']]], axis=1)
print(f"After II/246 cross-match: {len(df)} galaxies")


# II/356: GAMA DR3
df, gama_matched = cross_match(df, gama, 'objra_y', 'objdec', 'RA', 'Dec')
df = pd.concat([df, gama_matched[['Flux_Ha', 'Flux_NII_6584', 'e_Flux_Ha', 'u_mag', 'g_mag', 'r_mag', 'i_mag', 'z_mag']]], axis=1)
print(f"After II/356 cross-match: {len(df)} galaxies")


# Recompute log_SFR_Ha and metallicity from raw fluxes (using V/154 data)
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


# Add photometric colors (from V/147)
df['color_ug'] = df['petroMag_u'] - df['petroMag_g']
df['color_gr'] = df['petroMag_g'] - df['petroMag_r']
df['color_ri'] = df['petroMag_r'] - df['petroMag_i']
df['color_iz'] = df['petroMag_i'] - df['petroMag_z']
df['e_color_ug'] = np.sqrt(df['petroMagErr_u']**2 + df['petroMagErr_g']**2)
df['e_color_gr'] = np.sqrt(df['petroMagErr_g']**2 + df['petroMagErr_r']**2)


# Add 2MASS colors (from II/246)
df['color_JK'] = df['Jmag'] - df['Kmag']
df['e_color_JK'] = np.sqrt(df['e_Jmag']**2 + df['e_Kmag']**2)


# Drop rows with missing target or excessive NaNs
df = df.dropna(subset=["log_SFR_Ha"])
df = df.dropna(axis=0, thresh=int(0.8 * df.shape[1]))
df.fillna(df.median(numeric_only=True), inplace=True)


# Step 1: Cosmo-Rank Construction
gz_df = df.copy()
morph_cols = ['P(CD)', 'P(E)', 'P(S0)', 'P(Sa)', 'P(Sab)', 'P(Sb)', 'P(Sbc)', 
              'P(Sc)', 'P(Scd)', 'P(Sd)', 'P(Sdm)', 'P(Sm)', 'P(Irr)']
gz_df['morph_sum'] = gz_df[morph_cols].sum(axis=1)
gz_df['Num_w'] = gz_df['conf_prob']
scaler_rank = MinMaxScaler()
