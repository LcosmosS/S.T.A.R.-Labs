# S.T.A.R. Model for predicting log_SFR_Ha using the STAR framework

# STAR: Symbolicly. Tuned. Astronomical. Regressors.
# - S: Symbolic-Regression via gplearn
# - T: Tuned hyperparameter optimization with Optuna
# - A: Astronomical predictions of star formation rates in galaxies
# - R: Regressors - HistGradientBoostingRegressor, LightGBM, XGBoost, CatBoost

import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import HistGradientBoostingRegressor
from gplearn.genetic import SymbolicRegressor
import optuna
import warnings
from numpy.polynomial import Polynomial
from scipy.spatial import cKDTree
import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostRegressor

warnings.filterwarnings("ignore")

# Load the original dataset and ensure RA/Dec are numeric
df = pd.read_csv("merged_data.csv")
df['objra_y'] = pd.to_numeric(df['objra_y'], errors='coerce')
df['objdec'] = pd.to_numeric(df['objdec'], errors='coerce')
print(f"Initial df: objra_y dtype: {df['objra_y'].dtype}, objdec dtype: {df['objdec'].dtype}")
print(f"NaN in objra_y: {df['objra_y'].isna().sum()}, NaN in objdec: {df['objdec'].isna().sum()}")

# Load the SDSS datasets and merge them
sdss_dr16 = pd.read_csv("V154sdss16.csv")  # V/154: SDSS DR16
sdss_dr12 = pd.read_csv("V147sdss12.csv")  # V/147: SDSS DR12# Merge V/154 and V/147 on objID
sdss_merged = pd.merge(
    sdss_dr16[['objID', 'RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']],
    sdss_dr12[['objID', 'RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']],
    on='objID',
    how='outer',
    suffixes=('_dr16', '_dr12')
)

# Combine columns, preferring DR16 values where available, otherwise use DR12
sdss_merged['RA_ICRS'] = sdss_merged['RA_ICRS_dr16'].combine_first(sdss_merged['RA_ICRS_dr12'])
sdss_merged['DE_ICRS'] = sdss_merged['DE_ICRS_dr16'].combine_first(sdss_merged['DE_ICRS_dr12'])
sdss_merged['zsp'] = sdss_merged['zsp_dr16'].combine_first(sdss_merged['zsp_dr12'])
sdss_merged['umag'] = sdss_merged['umag_dr16'].combine_first(sdss_merged['umag_dr12'])
sdss_merged['gmag'] = sdss_merged['gmag_dr16'].combine_first(sdss_merged['gmag_dr12'])
sdss_merged['rmag'] = sdss_merged['rmag_dr16'].combine_first(sdss_merged['rmag_dr12'])
sdss_merged['imag'] = sdss_merged['imag_dr16'].combine_first(sdss_merged['imag_dr12'])
sdss_merged['zmag'] = sdss_merged['zmag_dr16'].combine_first(sdss_merged['zmag_dr12'])
sdss_merged['e_umag'] = sdss_merged['e_umag_dr16'].combine_first(sdss_merged['e_umag_dr12'])
sdss_merged['e_gmag'] = sdss_merged['e_gmag_dr16'].combine_first(sdss_merged['e_gmag_dr12'])
sdss_merged['e_rmag'] = sdss_merged['e_rmag_dr16'].combine_first(sdss_merged['e_rmag_dr12'])
sdss_merged['e_imag'] = sdss_merged['e_imag_dr16'].combine_first(sdss_merged['e_imag_dr12'])
sdss_merged['e_zmag'] = sdss_merged['e_zmag_dr16'].combine_first(sdss_merged['e_zmag_dr12'])

# Drop the intermediate columns
sdss_merged = sdss_merged[['objID', 'RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']]# Save the merged dataset for future use
sdss_merged.to_csv("sdss_merged.csv", index=False)
print(f"Merged SDSS dataset created with {len(sdss_merged)} rows.")# Print columns for debugging
print("Columns in merged_data.csv:", df.columns.tolist())
print("Columns in sdss_merged (V/147 + V/154):", sdss_merged.columns.tolist())

# Function to clean DataFrame by removing rows with NaN or inf in RA/Dec columns
def clean_coordinates(df, ra_col, dec_col):
    initial_len = len(df)
    mask = (
        df[ra_col].notna() & df[dec_col].notna() &  # Not NaN
        np.isfinite(df[ra_col]) & np.isfinite(df[dec_col])  # Not inf
    )
    df_cleaned = df[mask].copy()
    print(f"Removed {initial_len - len(df_cleaned)} rows from DataFrame due to NaN or inf in {ra_col} or {dec_col}")
    if len(df_cleaned) > 0:
        print(f"RA range in {ra_col}: {df_cleaned[ra_col].min():.4f} to {df_cleaned[ra_col].max():.4f}")
        print(f"Dec range in {dec_col}: {df_cleaned[dec_col].min():.4f} to {df_cleaned[dec_col].max():.4f}")
    else:
        print(f"No valid RA/Dec data after cleaning in {ra_col}/{dec_col}")
    return df_cleaned

# Cross-match function
def deg_to_rad(df, ra_col, dec_col):
    try:
        df['ra_rad'] = np.radians(df[ra_col])
        df['dec_rad'] = np.radians(df[dec_col])
        return df
    except KeyError as e:
        print(f"KeyError in deg_to_rad: {e}")
        print(f"Available columns in DataFrame: {df.columns.tolist()}")
        raise
def cross_match(df1, df2, ra_col1, dec_col1, ra_col2, dec_col2, max_dist_arcsec=10.0):
    try:
        df1_cleaned = clean_coordinates(df1, ra_col1, dec_col1)
        df2_cleaned = clean_coordinates(df2, ra_col2, dec_col2)
        if len(df1_cleaned) == 0 or len(df2_cleaned) == 0:
            print("One of the DataFrames is empty after cleaning. Cannot perform cross-match.")
            return df1_cleaned, pd.DataFrame()

        df1_cleaned = deg_to_rad(df1_cleaned, ra_col1, dec_col1)
        df2_cleaned = deg_to_rad(df2_cleaned, ra_col2, dec_col2)

        coords1 = np.array([df1_cleaned['ra_rad'], df1_cleaned['dec_rad']]).T
        coords2 = np.array([df2_cleaned['ra_rad'], df2_cleaned['dec_rad']]).T

        tree = cKDTree(coords2)
        max_dist = np.radians(max_dist_arcsec / 3600.0)
        dist, idx = tree.query(coords1, k=1, distance_upper_bound=max_dist)

        matched = dist < max_dist
        df1_matched = df1_cleaned[matched].copy()
        df2_matched = df2_cleaned.iloc[idx[matched]].copy()

        df1_matched = df1_matched.reset_index(drop=True)
        df2_matched = df2_matched.reset_index(drop=True)

        if len(df1_matched) > 0:
            print("Sample matches (first 5):")
            for i in range(min(5, len(df1_matched))):
                print(f"Match {i+1}: {ra_col1}={df1_matched[ra_col1].iloc[i]:.4f}, {dec_col1}={df1_matched[dec_col1].iloc[i]:.4f} "
                      f"matched to {ra_col2}={df2_matched[ra_col2].iloc[i]:.4f}, {dec_col2}={df2_matched[dec_col2].iloc[i]:.4f} "
                      f"(distance={(dist[matched][i] * 3600 * 180 / np.pi):.2f} arcsec)")
        else:
            print("No matches found within the specified radius.")

        return df1_matched, df2_matched
    except KeyError as e:  # Line 139 - Correctly indented
        print(f"KeyError in cross_match: {e}")
        print(f"df1 columns: {df1.columns.tolist()}")
        print(f"df2 columns: {df2.columns.tolist()}")
        raise
    except Exception as e:
        print(f"Error in cross_match: {e}")
        raise

        # Updated cross-match function for large datasets with NaN handling
def cross_match_in_chunks(df1, filepath, ra_col1, dec_col1, ra_col2, dec_col2, columns_to_keep, max_dist_arcsec=10.0, chunksize=100000):
    try:
        df1[ra_col1] = pd.to_numeric(df1[ra_col1], errors='coerce')
        df1[dec_col1] = pd.to_numeric(df1[dec_col1], errors='coerce')
        print(f"df1 RA range: {df1[ra_col1].min():.4f} to {df1[ra_col1].max():.4f}")
        print(f"df1 Dec range: {df1[dec_col1].min():.4f} to {df1[dec_col1].max():.4f}")
        print(f"df1 rows with valid RA/Dec: {df1[[ra_col1, dec_col1]].notna().all(axis=1).sum()}")

        min_ra, max_ra = df1[ra_col1].min() - 0.1, df1[ra_col1].max() + 0.1  # Line 148 - Correctly indented
        min_dec, max_dec = df1[dec_col1].min() - 0.1, df1[dec_col1].max() + 0.1
        
        if pd.isna([min_ra, max_ra, min_dec, max_dec]).any():
            print("Warning: NaN found in RA/Dec bounds. Replacing with defaults.")
            min_ra = 0 if pd.isna(min_ra) else min_ra
            max_ra = 360 if pd.isna(max_ra) else max_ra
            min_dec = -90 if pd.isna(min_dec) else min_dec
            max_dec = 90 if pd.isna(max_dec) else max_dec
        print(f"Filtering bounds: RA {min_ra:.4f} to {max_ra:.4f}, Dec {min_dec:.4f} to {max_dec:.4f}")

        matched_df2_list = []
        usecols = [ra_col2, dec_col2] + columns_to_keep
        
        chunk_reader = pd.read_csv(filepath, chunksize=chunksize, usecols=usecols, on_bad_lines='warn')
        for i, chunk in enumerate(chunk_reader):
            print(f"Processing chunk {i+1} with {len(chunk)} rows...")
            chunk[ra_col2] = pd.to_numeric(chunk[ra_col2], errors='coerce')
            chunk[dec_col2] = pd.to_numeric(chunk[dec_col2], errors='coerce')
            for col in columns_to_keep:
                chunk[col] = pd.to_numeric(chunk[col], errors='coerce')
            chunk = chunk.dropna(subset=[ra_col2, dec_col2])
            print(f"Chunk {i+1} after NaN removal: {len(chunk)} rows")
            if len(chunk) == 0:
                print(f"Chunk {i+1} empty after NaN removal.")
                continue
            
            chunk_filtered = chunk[
                (chunk[ra_col2] >= min_ra) & (chunk[ra_col2] <= max_ra) &
                (chunk[dec_col2] >= min_dec) & (chunk[dec_col2] <= max_dec)
            ]
            print(f"Chunk {i+1} after RA/Dec filter: {len(chunk_filtered)} rows")
            if len(chunk_filtered) == 0:
                continue
            
            _, matched_df2 = cross_match(df1, chunk_filtered, ra_col1, dec_col1, ra_col2, dec_col2, max_dist_arcsec)
            print(f"Chunk {i+1} matches found: {len(matched_df2)}")
            if len(matched_df2) > 0:
                matched_df2_list.append(matched_df2[columns_to_keep])
        
        if len(matched_df2_list) == 0:
            print("No matches found in any chunk.")
            return df1, pd.DataFrame()
        
        matched_df2 = pd.concat(matched_df2_list, ignore_index=True)
        matched_df1 = df1.copy()
        print(f"Final matched_df2 rows: {len(matched_df2)}")
        return matched_df1, matched_df2
    except Exception as e:
        print(f"Error in cross_match_in_chunks: {e}")
        raise
# Store the original DataFrame before cross-matching
df_original = df.copy()# Cross-match with VizieR catalogues
# SDSS merged dataset (V/147 + V/154)
df, sdss_matched = cross_match(df, sdss_merged, 'objra_y', 'objdec', 'RA_ICRS', 'DE_ICRS', max_dist_arcsec=10.0)
print(f"After SDSS cross-match: {len(df)} galaxies")
sdss_columns = ['zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']
if len(df) == 0:
    print("No matches found with SDSS merged data (V/147 + V/154). Falling back to original data and using nsa_z for redshift.")
    df = df_original.copy()
    df['zsp'] = df['nsa_z']
else:
    # Fill NaN with median for SDSS columns
    print(f"SDSS NaN counts before filling:\n{sdss_matched[sdss_columns].isna().sum()}")
    sdss_matched[sdss_columns] = sdss_matched[sdss_columns].fillna(sdss_matched[sdss_columns].median())
    print(f"SDSS NaN counts after filling:\n{sdss_matched[sdss_columns].isna().sum()}")
    df = pd.concat([df, sdss_matched[sdss_columns]], axis=1)
    print(f"SDSS matches found: {len(sdss_matched)}")
    
    # II/246: 2MASS Extended Source Catalogue
twomass_columns = ['Jmag', 'Hmag', 'Kmag', 'e_Jmag', 'e_Hmag', 'e_Kmag']
df, twomass_matched = cross_match_in_chunks(
    df, "2Mass.csv",
    'objra_y', 'objdec', 'RAJ2000', 'DEJ2000',
    twomass_columns,
    max_dist_arcsec=10.0, chunksize=100000
)
print(f"After II/246 cross-match: {len(df)} galaxies")
if len(df) > 0:
    # Fill NaN with median for 2MASS columns
    print(f"2MASS NaN counts before filling:\n{twomass_matched[twomass_columns].isna().sum()}")
    twomass_matched[twomass_columns] = twomass_matched[twomass_columns].fillna(twomass_matched[twomass_columns].median())
    print(f"2MASS NaN counts after filling:\n{twomass_matched[twomass_columns].isna().sum()}")
    df = pd.concat([df, twomass_matched[twomass_columns]], axis=1)
    
    # II/356: GAMA DR3
gama_columns = ['UmAB', 'BmAB', 'VmAB']
print("Starting GAMA DR3 cross-match...")
df, gama_matched = cross_match_in_chunks(
    df, "II356xmmom41s.csv",
    'objra_y', 'objdec', 'RAJ2000', 'DEJ2000',
    gama_columns,
    max_dist_arcsec=10.0, chunksize=100000
)
print(f"After II/356 cross-match: {len(df)} galaxies")
print(f"gama_matched length: {len(gama_matched)}")
print(f"gama_matched columns: {gama_matched.columns.tolist()}")
if len(gama_matched) > 0 and all(col in gama_matched.columns for col in gama_columns):
    # Fill NaN with median for GAMA columns
    print(f"GAMA NaN counts before filling:\n{gama_matched[gama_columns].isna().sum()}")
    gama_matched[gama_columns] = gama_matched[gama_columns].fillna(gama_matched[gama_columns].median())
    print(f"GAMA NaN counts after filling:\n{gama_matched[gama_columns].isna().sum()}")
    df = pd.concat([df, gama_matched[gama_columns]], axis=1)
else:
    print("No matches found for GAMA DR3 or columns missing, skipping concatenation.")
    # Print columns after cross-matching for debugging
    print("Columns in df after cross-matching:", df.columns.tolist())

# Recompute log_SFR_Ha and metallicity using fluxes from merged_data.csv
df['flux_Ha'] = df['F_Ha_cen']
df['e_flux_Ha'] = df['e_F_Ha_cen']
df['flux_Hb'] = df['flux_Hbeta4861.36_Re_fit']
df['flux_OIII_5007'] = df['flux_[OIII]5006.84_Re_fit']
df['flux_NII_6584'] = df['flux_[NII]6583.45_Re_fit']

# Check for NaN in flux columns and handle them
flux_cols = ['flux_Ha', 'flux_Hb', 'flux_OIII_5007', 'flux_NII_6584', 'e_flux_Ha']
for col in flux_cols:
    nan_count = df[col].isna().sum()
    print(f"NaN count in {col}: {nan_count}")
    if nan_count > 0:
        df[col] = df[col].fillna(df[col].median())

df['Ha_Hb_observed'] = df['flux_Ha'] / df['flux_Hb']  # Line 266 - Moved outside loop
Ha_Hb_intrinsic = 2.86
k_Ha = 2.468
k_Hb = 3.634
df['A_Ha'] = 2.5 * np.log10(df['Ha_Hb_observed'] / Ha_Hb_intrinsic) * (k_Ha / (k_Hb - k_Ha))
df['flux_Ha_corr'] = df['flux_Ha'] * 10**(0.4 * df['A_Ha'])
H0 = 70  # km/s/Mpc
c = 3e5  # km/s
df['DL'] = (c * df['zsp'] / H0) * 3.0856e24  # cm, using zsp
df['L_Ha'] = df['flux_Ha_corr'] * 4 * np.pi * df['DL']**2  # erg/s
df['log_SFR_Ha_raw'] = np.log10(df['L_Ha'] * 7.9e-42)  # M_sun/yr
df['log_O3N2_raw'] = np.log10((df['flux_OIII_5007'] / df['flux_Hb']) / (df['flux_NII_6584'] / df['flux_Ha']))
df['OH_O3N2_raw'] = 8.533 - 0.214 * df['log_O3N2_raw']
print(f"NaN in L_Ha: {df['L_Ha'].isna().sum()}")
print(f"NaN in log_SFR_Ha_raw: {df['log_SFR_Ha_raw'].isna().sum()}")

# Add raw fluxes as features
df['log_flux_Ha'] = np.log10(df['flux_Ha'] + 1e-10)
df['log_flux_Hb'] = np.log10(df['flux_Hb'] + 1e-10)
df['log_flux_OIII_5007'] = np.log10(df['flux_OIII_5007'] + 1e-10)
df['log_flux_NII_6584'] = np.log10(df['flux_NII_6584'] + 1e-10)
df['log_e_flux_Ha'] = np.log10(df['e_flux_Ha'] + 1e-10)

# Add photometric colors (if available)
if 'umag' in df.columns:
    df['color_ug'] = df['umag'] - df['gmag']
    df['color_gr'] = df['gmag'] - df['rmag']
    df['color_ri'] = df['rmag'] - df['imag']
    df['color_iz'] = df['imag'] - df['zmag']
    df['e_color_ug'] = np.sqrt(df['e_umag']**2 + df['e_gmag']**2)
    df['e_color_gr'] = np.sqrt(df['e_gmag']**2 + df['e_rmag']**2)

if 'Jmag' in df.columns:  # Line 298 - Moved to new line, dedented
    df['color_JK'] = df['Jmag'] - df['Kmag']
    df['e_color_JK'] = np.sqrt(df['e_Jmag']**2 + df['e_Kmag']**2)
    
# Drop rows with missing target or excessive NaNs, then fill remaining NaNs
df = df.dropna(subset=["log_SFR_Ha_raw"])
df = df.dropna(axis=0, thresh=int(0.5 * df.shape[1]))  # 50% non-NaN

# Step 1: Cosmo-Rank Construction
gz_df = df.copy()
morph_cols = ['P(CD)', 'P(E)', 'P(S0)', 'P(Sa)', 'P(Sab)', 'P(Sb)', 'P(Sbc)', 
              'P(Sc)', 'P(Scd)', 'P(Sd)', 'P(Sdm)', 'P(Sm)', 'P(Irr)']
gz_df['morph_sum'] = gz_df[morph_cols].sum(axis=1)
gz_df['Num_w'] = gz_df['conf_prob']
scaler_rank = MinMaxScaler()
gz_df[['morph_sum_norm', 'Num_w_norm', 'nsa_z_norm']] = scaler_rank.fit_transform(
    gz_df[['morph_sum', 'Num_w', 'nsa_z']]
)
gz_df['cosmo_rank'] = (0.5 * gz_df['Num_w_norm'] + 0.3 * gz_df['morph_sum_norm'] + 0.2 * gz_df['nsa_z_norm'])
df['cosmo_rank'] = gz_df['cosmo_rank']

# Step 2: L_cosmo(s) Construction
alpha = -1.5
M_star = df['log_Mass_gas'].median()
df['a_n'] = (10 ** df['log_Mass_gas'])**(1 + alpha) * np.exp(-10 ** df['log_Mass_gas'] / (10 ** M_star))
bins = pd.qcut(df['Re_kpc'], q=20, labels=False, duplicates='drop') + 1
df['z_bin'] = bins
n_bins = df['z_bin'].nunique()
print(f"Number of unique bins after qcut: {n_bins}")
print("Bin distribution for Re_kpc (after qcut):")
print(df['z_bin'].value_counts().sort_index())
s_vals = [0.5, 1.0, 1.5, 2.0]
s_range = np.linspace(0.5, 2, 50)
for s in s_vals:
    col_name = f'L_cosmo_s_{s:.1f}'
    df[col_name] = df.groupby('z_bin')['a_n'].transform('mean') / (df['z_bin'] ** s)
print("Columns after creating L_cosmo_s*:")
print(df.columns.tolist())
print("Checking for NaN/infinite values in cosmo_rank and L_cosmo_s_1.0:")
print("cosmo_rank NaN count:", df['cosmo_rank'].isna().sum())
print("L_cosmo_s_1.0 NaN count:", df['L_cosmo_s_1.0'].isna().sum())
print("cosmo_rank infinite count:", np.isinf(df['cosmo_rank']).sum())
print("L_cosmo_s_1.0 infinite count:", np.isinf(df['L_cosmo_s_1.0']).sum())
df['cosmo_rank_L'] = df['cosmo_rank'] * df['L_cosmo_s_1.0']
df['cosmo_rank_L'] = df['cosmo_rank_L'].replace([np.inf, -np.inf], np.nan).fillna(0)
print("cosmo_rank_L created, NaN count:", df['cosmo_rank_L'].isna().sum())

# Plot L_cosmo(s) vs s
grouped_means = df.groupby('z_bin')['a_n'].mean().reindex(range(1, n_bins + 1), fill_value=0)
L_vals = [grouped_means / (np.arange(1, n_bins + 1) ** s) for s in s_range]
L_vals = np.array([sum(l) for l in L_vals])
plt.plot(s_range, L_vals)
plt.xlabel("s")
plt.ylabel("L_cosmo(s)")
plt.title("L_cosmo(s) Behavior")
plt.savefig("L_cosmo_curve.png")
plt.close()

# Scatter plot of L_cosmo_s_1.0 vs log_SFR_Ha
plt.scatter(df['L_cosmo_s_1.0'], df['log_SFR_Ha'], alpha=0.5)
plt.xlabel("L_cosmo_s_1.0")
plt.ylabel("log_SFR_Ha")
plt.title("L_cosmo_s_1.0 vs log_SFR_Ha")
plt.savefig("L_cosmo_s1_vs_SFR.png")
plt.close()

# Step 3: Define features and target
target = "log_SFR_Ha"  # Adjust to "log_SFR_Ha_raw" if that’s your intended target
base_features = [
    "log_Mass_gas", "log_Mass", "Av_gas_Re", "Av_ssp_Re", 
    "OH_O3N2_cen", "OH_T04_cen", "OH_dop_cen", "Age_LW_Re_fit", 
    "ZH_LW_Re_fit", "Re_kpc", "vel_disp_Ha_cen", "Lambda_Re", 
    "Sigma_Mass_Re", "EW_Ha_cen", "Ha_Hb_cen"
]
# Assuming df is loaded earlier with 1,000,000 rows
print(f"Initial rows in df: {len(df)}")

# Step 3: Define features and target
target = "log_SFR_Ha_raw"  # Using log_SFR_Ha_raw as per your output
base_features = [
    "log_Mass_gas", "log_Mass", "Av_gas_Re", "Av_ssp_Re", 
    "OH_O3N2_cen", "OH_T04_cen", "OH_dop_cen", "Age_LW_Re_fit", 
    "ZH_LW_Re_fit", "Re_kpc", "vel_disp_Ha_cen", "Lambda_Re", 
    "Sigma_Mass_Re", "EW_Ha_cen", "Ha_Hb_cen"
]
# Feature engineering
df["mass_metallicity"] = df["log_Mass"] * df["OH_O3N2_cen"]
df["dust_metallicity"] = df["Av_gas_Re"] * df["OH_T04_cen"]
df["disp_mass_ratio"] = df["vel_disp_Ha_cen"] / (df["Sigma_Mass_Re"] + 1e-5)
df["age_metallicity"] = df["Age_LW_Re_fit"] * df["ZH_LW_Re_fit"]
df["sqrt_Re_kpc"] = np.sqrt(df['Re_kpc'] + 1e-5)
df["log_mass"] = np.log(df["log_Mass_gas"] + 1e-5)
df["BSD_likelihood"] = (
    df["log_Mass_gas"] * df["OH_O3N2_cen"] /
    (df["Av_gas_Re"] + 1e-5 + df["Age_LW_Re_fit"])
)
df["cosmo_rank_mass"] = df["cosmo_rank"] * df["log_Mass"]
df["L_cosmo_s1_mass"] = df["L_cosmo_s_1.0"] * df["log_Mass"]
df["cosmo_rank_EW"] = df["cosmo_rank"] * df["EW_Ha_cen"]
df["L_cosmo_s1_EW"] = df["L_cosmo_s_1.0"] * df["EW_Ha_cen"]
df["cosmo_rank_scaled"] = df["cosmo_rank"] * 20
df["L_cosmo_s1_scaled"] = df["L_cosmo_s_1.0"] * 20
df["cosmo_rank_L_mass"] = df["cosmo_rank_L"] * df["log_Mass"]
df["L_cosmo_s1_metallicity"] = df["L_cosmo_s_1.0"] * df["OH_O3N2_cen"]
features = base_features + [
    "mass_metallicity", "dust_metallicity", "disp_mass_ratio", 
    "age_metallicity", "sqrt_Re_kpc", "log_mass", "BSD_likelihood", 
    "cosmo_rank", "L_cosmo_s_0.5", "L_cosmo_s_1.5", "L_cosmo_s_2.0", 
    "cosmo_rank_L", "cosmo_rank_mass", "L_cosmo_s1_mass",
    "cosmo_rank_EW", "L_cosmo_s1_EW", "cosmo_rank_scaled", "L_cosmo_s1_scaled",
    "cosmo_rank_L_mass", "L_cosmo_s1_metallicity",
    "log_flux_Ha", "log_flux_Hb", "log_flux_OIII_5007", "log_flux_NII_6584", 
    "log_e_flux_Ha", "log_SFR_Ha_raw", "OH_O3N2_raw"
]
if 'color_ug' in df.columns:
    features.extend(["color_ug", "color_gr", "color_ri", "color_iz", "e_color_ug", "e_color_gr"])
if 'color_JK' in df.columns:
    features.extend(["color_JK", "e_color_JK"])

# Select features and target
print(f"Features defined: {features}")
X = df[features]
y = df[target]
print(f"Rows after feature selection: {len(X)}")
print(f"NaN in y ({target}): {y.isna().sum()}")

# Filter to numeric columns only
numeric_features = [col for col in features if pd.api.types.is_numeric_dtype(X[col])]
X = X[numeric_features]
print(f"Numeric features selected: {numeric_features}")
print("Sample values:")
print(X.head())

# Clean X and y
X = X.replace([np.inf, -np.inf], np.nan)
print(f"Columns with NaN before imputation: {X.columns[X.isna().any()].tolist()}")
X = X.fillna(X.median())  # Impute NaN with column medians
print(f"Rows after X imputation: {len(X)}")
y = y.replace([np.inf, -np.inf], np.nan)
print(f"Rows before y.dropna(): {len(y)}")
y = y.dropna()
print(f"Rows after y.dropna(): {len(y)}")
mask = y.index.isin(X.index)
X = X.loc[mask]
y = y.loc[mask]
print(f"Rows after NaN/infinity cleaning: {len(X)}")

# Train/test split
if len(X) < 10:
    raise ValueError(f"Only {len(X)} rows after cleaning. Check data preprocessing.")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Verify inputs
print("NaN in X_train_scaled:", np.isnan(X_train_scaled).sum())
print("Inf in X_train_scaled:", np.isinf(X_train_scaled).sum())
print("NaN in y_train:", y_train.isna().sum())
print("Inf in y_train:", np.isinf(y_train).sum())

# Optuna optimization for HistGradientBoostingRegressor
def objective_hgb(trial):
    params = {
        'max_iter': trial.suggest_int('max_iter', 100, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
        'l2_regularization': trial.suggest_float('l2_regularization', 0.1, 10.0),
        'max_leaf_nodes': trial.suggest_int('max_leaf_nodes', 20, 50),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 10, 30),
        'random_state': 42
    }
    model = HistGradientBoostingRegressor(**params)
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='r2')
    mean_score = np.nanmean(scores)  # Handle NaN in scores
    if np.isnan(mean_score):
        print(f"HGB Trial {trial.number} failed: scores = {scores}")
    return mean_score if not np.isnan(mean_score) else -np.inf

study_hgb = optuna.create_study(direction='maximize')
study_hgb.optimize(objective_hgb, n_trials=20)
best_params_hgb = study_hgb.best_params
print("Best HistGradientBoosting Parameters:", best_params_hgb)
print("Best HistGradientBoosting CV R²:", study_hgb.best_value)

# Train HistGradientBoostingRegressor
hgb = HistGradientBoostingRegressor(**best_params_hgb, random_state=42)
hgb.fit(X_train_scaled, y_train)
y_pred_hgb = hgb.predict(X_test_scaled)
r2_hgb = r2_score(y_test, y_pred_hgb)
cv_scores_hgb = cross_val_score(hgb, X_train_scaled, y_train, cv=5, scoring='r2')
print(f"HistGradientBoosting 5-Fold CV R²: Mean = {cv_scores_hgb.mean():.4f}, Std = {cv_scores_hgb.std():.4f}")
print(f"R^2 Score (HistGradientBoosting, Test): {r2_hgb:.4f}")

# Optuna optimization for LightGBM
def objective_lgb(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
        'num_leaves': trial.suggest_int('num_leaves', 20, 50),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
        'reg_lambda': trial.suggest_float('reg_lambda', 0.1, 10.0),
        'random_state': 42,
        'verbose': -1
    }
    model = lgb.LGBMRegressor(**params)
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='r2')
    mean_score = np.nanmean(scores)
    if np.isnan(mean_score):
        print(f"LGB Trial {trial.number} failed: scores = {scores}")
    return mean_score if not np.isnan(mean_score) else -np.inf

study_lgb = optuna.create_study(direction='maximize')
study_lgb.optimize(objective_lgb, n_trials=20)
best_params_lgb = study_lgb.best_params
print("Best LightGBM Parameters:", best_params_lgb)
print("Best LightGBM CV R²:", study_lgb.best_value)

# Train LightGBM
lgb_model = lgb.LGBMRegressor(**best_params_lgb, random_state=42, verbose=-1)
lgb_model.fit(X_train_scaled, y_train)
y_pred_lgb = lgb_model.predict(X_test_scaled)
r2_lgb = r2_score(y_test, y_pred_lgb)
cv_scores_lgb = cross_val_score(lgb_model, X_train_scaled, y_train, cv=5, scoring='r2')
print(f"LightGBM 5-Fold CV R²: Mean = {cv_scores_lgb.mean():.4f}, Std = {cv_scores_lgb.std():.4f}")
print(f"R^2 Score (LightGBM, Test): {r2_lgb:.4f}")

# XGBoost Optimization
def objective_xgb(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
        'reg_lambda': trial.suggest_float('reg_lambda', 0.1, 10.0),
        'random_state': 42
    }
    model = xgb.XGBRegressor(**params)
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='r2')
    mean_score = np.nanmean(scores)
    if np.isnan(mean_score):
        print(f"XGB Trial {trial.number} failed: scores = {scores}")
    return mean_score if not np.isnan(mean_score) else -np.inf

study_xgb = optuna.create_study(direction='maximize')
study_xgb.optimize(objective_xgb, n_trials=20)
best_params_xgb = study_xgb.best_params
print("Best XGBoost Parameters:", best_params_xgb)
print("Best XGBoost CV R²:", study_xgb.best_value)

# Train XGBoost
xgb_model = xgb.XGBRegressor(**best_params_xgb, random_state=42)
xgb_model.fit(X_train_scaled, y_train)
y_pred_xgb = xgb_model.predict(X_test_scaled)
r2_xgb = r2_score(y_test, y_pred_xgb)
cv_scores_xgb = cross_val_score(xgb_model, X_train_scaled, y_train, cv=5, scoring='r2')
print(f"XGBoost 5-Fold CV R²: Mean = {cv_scores_xgb.mean():.4f}, Std = {cv_scores_xgb.std():.4f}")
print(f"R^2 Score (XGBoost, Test): {r2_xgb:.4f}")

# CatBoost Optimization
def objective_cat(trial):
    params = {
        'iterations': trial.suggest_int('iterations', 100, 500),
        'depth': trial.suggest_int('depth', 4, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
        'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1, 10),
        'random_seed': 42,
        'verbose': 0
    }
    model = CatBoostRegressor(**params)
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='r2')
    mean_score = np.nanmean(scores)
    if np.isnan(mean_score):
        print(f"Cat Trial {trial.number} failed: scores = {scores}")
    return mean_score if not np.isnan(mean_score) else -np.inf

study_cat = optuna.create_study(direction='maximize')
study_cat.optimize(objective_cat, n_trials=20)
best_params_cat = study_cat.best_params
print("Best CatBoost Parameters:", best_params_cat)
print("Best CatBoost CV R²:", study_cat.best_value)

# Train CatBoost
cat_model = CatBoostRegressor(**best_params_cat, random_seed=42, verbose=0)
cat_model.fit(X_train_scaled, y_train)
y_pred_cat = cat_model.predict(X_test_scaled)
r2_cat = r2_score(y_test, y_pred_cat)
cv_scores_cat = cross_val_score(cat_model, X_train_scaled, y_train, cv=5, scoring='r2')
print(f"CatBoost 5-Fold CV R²: Mean = {cv_scores_cat.mean():.4f}, Std = {cv_scores_cat.std():.4f}")
print(f"R^2 Score (CatBoost, Test): {r2_cat:.4f}")

# SHAP for feature selection
explainer_hgb = shap.Explainer(hgb, X_train_scaled)
shap_values_hgb = explainer_hgb(X_test_scaled)
explainer_lgb = shap.Explainer(lgb_model, X_train_scaled)
shap_values_lgb = explainer_lgb(X_test_scaled)
explainer_xgb = shap.Explainer(xgb_model, X_train_scaled)
shap_values_xgb = explainer_xgb(X_test_scaled)
explainer_cat = shap.Explainer(cat_model, X_train_scaled)
shap_values_cat = explainer_cat(X_test_scaled)

# Compute SHAP values for all models
explainer_hgb = shap.Explainer(hgb, X_train_scaled)  # Define explainer first
shap_values_hgb = explainer_hgb(X_test_scaled)       # Then compute SHAP values

explainer_lgb = shap.Explainer(lgb_model, X_train_scaled)
shap_values_lgb = explainer_lgb(X_test_scaled)

explainer_xgb = shap.Explainer(xgb_model, X_train_scaled)
shap_values_xgb = explainer_xgb(X_test_scaled)

explainer_cat = shap.Explainer(cat_model, X_train_scaled)
shap_values_cat = explainer_cat(X_test_scaled)

# SHAP summary plots
shap.summary_plot(shap_values_hgb, X_test_scaled, plot_type="bar", show=False)
plt.title("SHAP Summary - HistGradientBoosting")
plt.tight_layout()
plt.savefig("shap_hgb_summary.png")
plt.clf()

shap.summary_plot(shap_values_lgb, X_test_scaled, plot_type="bar", show=False)
plt.title("SHAP Summary - LightGBM")
plt.tight_layout()
plt.savefig("shap_lgb_summary.png")
plt.clf()

shap.summary_plot(shap_values_xgb, X_test_scaled, plot_type="bar", show=False)
plt.title("SHAP Summary - XGBoost")
plt.tight_layout()
plt.savefig("shap_xgb_summary.png")
plt.clf()

shap.summary_plot(shap_values_cat, X_test_scaled, plot_type="bar", show=False)
plt.title("SHAP Summary - CatBoost")
plt.tight_layout()
plt.savefig("shap_cat_summary.png")
plt.clf()  # Fixed: Added closing parenthesis

