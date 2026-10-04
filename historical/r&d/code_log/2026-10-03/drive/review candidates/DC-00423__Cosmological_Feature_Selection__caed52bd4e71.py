# STAR.py: Model for predicting log_SFR_Ha using the STAR framework # STAR: Symbolic, Tuned (Optuna), Astronomy Regressors (Random Forest + Gradient Boosting) # - S: Symbolic Regressor (via gplearn) # - T: Tuned (hyperparameter optimization with Optuna) # - A: Astronomy (predicting star formation rates in galaxies) # - R: Regressors (Random Forest and Gradient Boosting)
import pandas as pd import numpy as np import shap import matplotlib.pyplot as plt import seaborn as sns from sklearn.model_selection import train_test_split, cross_val_score, KFold from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor from sklearn.metrics import r2_score from sklearn.preprocessing import StandardScaler, MinMaxScaler from gplearn.genetic import SymbolicRegressor import optuna import warnings from numpy.polynomial import Polynomial from scipy.spatial import cKDTree
warnings.filterwarnings("ignore")
# Load the original dataset
df = pd.read_csv("merged_data.csv")
# Load VizieR data (update paths as needed)
sdss_spec = pd.read_csv("sdss_dr16_spec.csv") # V/154: Spectroscopic data sdss_photo = pd.read_csv("sdss_dr12_photo.csv") # V/147: Photometric data twomass = pd.read_csv("2mass_xsc.csv") # II/246: 2MASS Extended Source Catalogue gama = pd.read_csv("gama_dr3.csv") # II/356: GAMA DR3
# Print columns for debugging
print("Columns in merged_data.csv:", df.columns.tolist()) print("Columns in sdss_spec (V/154):", sdss_spec.columns.tolist()) print("Columns in sdss_photo (V/147):", sdss_photo.columns.tolist()) print("Columns in twomass (II/246):", twomass.columns.tolist()) print("Columns in gama (II/356):", gama.columns.tolist())
# Function to clean DataFrame by removing rows with NaN or inf in RA/Dec columns
def clean_coordinates(df, ra_col, dec_col): initial_len = len(df) # Check for NaN or inf in RA and Dec columns mask = ( df[ra_col].notna() & df[dec_col].notna() & # Not NaN np.isfinite(df[ra_col]) & np.isfinite(df[dec_col]) # Not inf ) df_cleaned = df[mask].copy() print(f"Removed {initial_len - len(df_cleaned)} rows from DataFrame due to NaN or inf in {ra_col} or {dec_col}") return df_cleaned
# Cross-match function
def deg_to_rad(df, ra_col, dec_col): try: df['ra_rad'] = np.radians(df[ra_col]) df['dec_rad'] = np.radians(df[dec_col]) return df except KeyError as e: print(f"KeyError in deg_to_rad: {e}") print(f"Available columns in DataFrame: {df.columns.tolist()}") raise
def cross_match(df1, df2, ra_col1, dec_col1, ra_col2, dec_col2, max_dist_arcsec=1.0): try: # Clean DataFrames to remove rows with NaN or inf in RA/Dec df1_cleaned = clean_coordinates(df1, ra_col1, dec_col1) df2_cleaned = clean_coordinates(df2, ra_col2, dec_col2)
   # Convert degrees to radians
    df1_cleaned = deg_to_rad(df1_cleaned, ra_col1, dec_col1)
    df2_cleaned = deg_to_rad(df2_cleaned, ra_col2, dec_col2)


    # Create coordinate arrays
    coords1 = np.array([df1_cleaned['ra_rad'], df1_cleaned['dec_rad']]).T
    coords2 = np.array([df2_cleaned['ra_rad'], df2_cleaned['dec_rad']]).T


    # Perform cross-match using cKDTree
    tree = cKDTree(coords2)
    max_dist = np.radians(max_dist_arcsec / 3600.0)
    dist, idx = tree.query(coords1, k=1, distance_upper_bound=max_dist)


    # Filter matches within the maximum distance
    matched = dist < max_dist
    df1_matched = df1_cleaned[matched].copy()
    df2_matched = df2_cleaned.iloc[idx[matched]].copy()


    # Reset indices
    df1_matched = df1_matched.reset_index(drop=True)
    df2_matched = df2_matched.reset_index(drop=True)


    return df1_matched, df2_matched
except KeyError as e:
    print(f"KeyError in cross_match: {e}")
    print(f"df1 columns: {df1.columns.tolist()}")
    print(f"df2 columns: {df2.columns.tolist()}")
    raise
except Exception as e:
    print(f"Error in cross_match: {e}")
    raise
# Cross-match with VizieR catalogues # V/154: SDSS DR16 spectroscopic data (uses RA_ICRS, DE_ICRS)
df, sdss_spec_matched = cross_match(df, sdss_spec, 'objra_y', 'objdec', 'RA_ICRS', 'DE_ICRS') df = pd.concat([df, sdss_spec_matched[['zsp']]], axis=1) # Use zsp instead of specz print(f"After V/154 cross-match: {len(df)} galaxies")
# V/147: SDSS DR12 photometric data (uses RA_ICRS, DE_ICRS)
df, sdss_photo_matched = cross_match(df, sdss_photo, 'objra_y', 'objdec', 'RA_ICRS', 'DE_ICRS') df = pd.concat([df, sdss_photo_matched[['umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']]], axis=1) print(f"After V/147 cross-match: {len(df)} galaxies")
# II/246: 2MASS Extended Source Catalogue (uses RAJ2000, DEJ2000)
df, twomass_matched = cross_match(df, twomass, 'objra_y', 'objdec', 'RAJ2000', 'DEJ2000') df = pd.concat([df, twomass_matched[['Jmag', 'Hmag', 'Kmag', 'e_Jmag', 'e_Hmag', 'e_Kmag']]], axis=1) print(f"After II/246 cross-match: {len(df)} galaxies")
# II/356: GAMA DR3 (uses RAJ2000, DEJ2000)
df, gama_matched = cross_match(df, gama, 'objra_y', 'objdec', 'RAJ2000', 'DEJ2000') df = pd.concat([df, gama_matched[['F(U)', 'F(B)', 'F(V)', 'UmAB', 'BmAB', 'VmAB']]], axis=1) print(f"After II/356 cross-match: {len(df)} galaxies")
# Recompute log_SFR_Ha and metallicity using fluxes from merged_data.csv
df['flux_Ha'] = df['F_Ha_cen'] # Use F_Ha_cen as flux_Ha df['e_flux_Ha'] = df['e_F_Ha_cen'] df['flux_Hb'] = df['flux_Hbeta4861.36_Re_fit'] df['flux_OIII_5007'] = df['flux_[OIII]5006.84_Re_fit'] df['flux_NII_6584'] = df['flux_[NII]6583.45_Re_fit']
df['Ha_Hb_observed'] = df['flux_Ha'] / df['flux_Hb'] Ha_Hb_intrinsic = 2.86 k_Ha = 2.468 k_Hb = 3.634 df['A_Ha'] = 2.5 * np.log10(df['Ha_Hb_observed'] / Ha_Hb_intrinsic) * (k_Ha / (k_Hb - k_Ha)) df['flux_Ha_corr'] = df['flux_Ha'] * 10**(0.4 * df['A_Ha']) H0 = 70 # km/s/Mpc c = 3e5 # km/s df['DL'] = (c * df['zsp'] / H0) * 3.0856e24 # cm, using zsp df['L_Ha'] = df['flux_Ha_corr'] * 4 * np.pi * df['DL']**2 # erg/s df['log_SFR_Ha_raw'] = np.log10(df['L_Ha'] * 7.9e-42) # M_sun/yr df['log_O3N2_raw'] = np.log10((df['flux_OIII_5007'] / df['flux_Hb']) / (df['flux_NII_6584'] / df['flux_Ha'])) df['OH_O3N2_raw'] = 8.533 - 0.214 * df['log_O3N2_raw']
# Add raw fluxes as features
df['log_flux_Ha'] = np.log10(df['flux_Ha'] + 1e-10) df['log_flux_Hb'] = np.log10(df['flux_Hb'] + 1e-10) df['log_flux_OIII_5007'] = np.log10(df['flux_OIII_5007'] + 1e-10) df['log_flux_NII_6584'] = np.log10(df['flux_NII_6584'] + 1e-10) df['log_e_flux_Ha'] = np.log10(df['e_flux_Ha'] + 1e-10)
# Add photometric colors (from V/147)
df['color_ug'] = df['umag'] - df['gmag'] df['color_gr'] = df['gmag'] - df['rmag'] df['color_ri'] = df['rmag'] - df['imag'] df['color_iz'] = df['imag'] - df['zmag'] df['e_color_ug'] = np.sqrt(df['e_umag']**2 + df['e_gmag']**2) df['e_color_gr'] = np.sqrt(df['e_gmag']**2 + df['e_rmag']**2)
# Add 2MASS colors (from II/246)
df['color_JK'] = df['Jmag'] - df['Kmag'] df['e_color_JK'] = np.sqrt(df['e_Jmag']**2 + df['e_Kmag']**2)
# Drop rows with missing target or excessive NaNs
df = df.dropna(subset=["log_SFR_Ha"]) df = df.dropna(axis=0, thresh=int(0.8 * df.shape[1])) df.fillna(df.median(numeric_only=True), inplace=True)
# Step 1: Cosmo-Rank Construction
gz_df = df.copy() morph_cols = ['P(CD)', 'P(E)', 'P(S0)', 'P(Sa)', 'P(Sab)', 'P(Sb)', 'P(Sbc)', 'P(Sc)', 'P(Scd)', 'P(Sd)', 'P(Sdm)', 'P(Sm)', 'P(Irr)'] gz_df['morph_sum'] = gz_df[morph_cols].sum(axis=1) gz_df['Num_w'] = gz_df['conf_prob'] scaler_rank = MinMaxScaler() gz_df[['morph_sum_norm', 'Num_w_norm', 'nsa_z_norm']] = scaler_rank.fit_transform( gz_df[['morph_sum', 'Num_w', 'nsa_z']] ) gz_df['cosmo_rank'] = (0.5 * gz_df['Num_w_norm'] + 0.3 * gz_df['morph_sum_norm'] + 0.2 * gz_df['nsa_z_norm']) df['cosmo_rank'] = gz_df['cosmo_rank']
# Step 2: L_cosmo(s) Construction
alpha = -1.5 M_star = df['log_Mass_gas'].median() df['a_n'] = (10 ** df['log_Mass_gas'])**(1 + alpha) * np.exp(-10 ** df['log_Mass_gas'] / (10 ** M_star)) bins = pd.qcut(df['Re_kpc'], q=20, labels=False, duplicates='drop') + 1 df['z_bin'] = bins n_bins = df['z_bin'].nunique() print(f"Number of unique bins after qcut: {n_bins}") print("Bin distribution for Re_kpc (after qcut):") print(df['z_bin'].value_counts().sort_index())
s_vals = [0.5, 1.0, 1.5, 2.0] s_range
