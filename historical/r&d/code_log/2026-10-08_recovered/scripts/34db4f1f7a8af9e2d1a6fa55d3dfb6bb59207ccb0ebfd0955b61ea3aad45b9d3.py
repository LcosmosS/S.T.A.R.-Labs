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
from scipy.spatial import cKDTree
import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostRegressor
from astropy.coordinates import SkyCoord
import astropy.units as u

warnings.filterwarnings("ignore")

# Load the original dataset and ensure RA/Dec are numeric
df = pd.read_csv("merged_data.csv")
df['objra_y'] = pd.to_numeric(df['objra_y'], errors='coerce')
df['objdec'] = pd.to_numeric(df['objdec'], errors='coerce')
print(f"Initial rows in merged_data.csv: {len(df)}")
print(f"NaN in objra_y: {df['objra_y'].isna().sum()}, NaN in objdec: {df['objdec'].isna().sum()}")

# Impute RA/Dec NaN with medians
df['objra_y'] = df['objra_y'].replace([np.inf, -np.inf], np.nan).fillna(df['objra_y'].median(skipna=True))
df['objdec'] = df['objdec'].replace([np.inf, -np.inf], np.nan).fillna(df['objdec'].median(skipna=True))
print(f"Rows after RA/Dec imputation: {len(df)}")

# Load and merge SDSS datasets
sdss_dr16 = pd.read_csv("V154sdss16.csv")
sdss_dr12 = pd.read_csv("V147sdss12.csv")
sdss_merged = pd.merge(
    sdss_dr16[['objID', 'RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']],
    sdss_dr12[['objID', 'RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']],
    on='objID',
    how='outer',
    suffixes=('_dr16', '_dr12')
)
for col in ['RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']:
    sdss_merged[col] = sdss_merged[f'{col}_dr16'].combine_first(sdss_merged[f'{col}_dr12'])
sdss_merged = sdss_merged[['objID', 'RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']]
sdss_merged.to_csv("sdss_merged.csv", index=False)
print(f"Merged SDSS dataset created with {len(sdss_merged)} rows.")
print("Columns in merged_data.csv:", df.columns.tolist())
print("Columns in sdss_merged (V/147 + V/154):", sdss_merged.columns.tolist())

# Before cross-matching
df = df.drop_duplicates(subset=['objra_y', 'objdec'], keep='first')
print(f"Rows after deduplication of df: {len(df)}")

# Cross-match functions
def clean_coordinates(df, ra_col, dec_col):
    initial_len = len(df)
    mask = (df[ra_col].notna() & df[dec_col].notna() & np.isfinite(df[ra_col]) & np.isfinite(df[dec_col]))
    df_cleaned = df[mask].copy()
    print(f"Removed {initial_len - len(df_cleaned)} rows from DataFrame due to NaN or inf in {ra_col} or {dec_col}")
    if len(df_cleaned) > 0:
        print(f"RA range in {ra_col}: {df_cleaned[ra_col].min():.4f} to {df_cleaned[ra_col].max():.4f}")
        print(f"Dec range in {dec_col}: {df_cleaned[dec_col].min():.4f} to {df_cleaned[dec_col].max():.4f}")
    else:
        print(f"No valid RA/Dec data after cleaning in {ra_col}/{dec_col}")
    return df_cleaned

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
    except Exception as e:
        print(f"Error in cross_match: {e}")
        raise

def cross_match_in_chunks(df1, filepath, ra_col1, dec_col1, ra_col2, dec_col2, columns_to_keep, max_dist_arcsec=10.0, chunksize=100000):
    try:
        df1[ra_col1] = pd.to_numeric(df1[ra_col1], errors='coerce').fillna(df1[ra_col1].median(skipna=True))
        df1[dec_col1] = pd.to_numeric(df1[dec_col1], errors='coerce').fillna(df1[dec_col1].median(skipna=True))
        min_ra, max_ra = df1[ra_col1].min() - 0.1, df1[ra_col1].max() + 0.1
        min_dec, max_dec = df1[dec_col1].min() - 0.1, df1[dec_col1].max() + 0.1
        print(f"Cross-matching bounds: RA {min_ra:.4f}-{max_ra:.4f}, Dec {min_dec:.4f}-{max_dec:.4f}")
        usecols = [ra_col2, dec_col2] + columns_to_keep
        chunk_reader = pd.read_csv(filepath, chunksize=chunksize, usecols=usecols, on_bad_lines='warn')
        matched_df2_list = []
        for i, chunk in enumerate(chunk_reader):
            print(f"Chunk {i+1} raw dtypes: {chunk[[ra_col2, dec_col2]].dtypes}")
            print(f"Chunk {i+1} raw sample:\n{chunk[[ra_col2, dec_col2]].head()}")
            chunk[ra_col2] = pd.to_numeric(chunk[ra_col2], errors='coerce')
            chunk[dec_col2] = pd.to_numeric(chunk[dec_col2], errors='coerce')
            for col in columns_to_keep:
                chunk[col] = pd.to_numeric(chunk[col], errors='coerce')
            print(f"Chunk {i+1} converted dtypes: {chunk[[ra_col2, dec_col2]].dtypes}")
            chunk = chunk.dropna(subset=[ra_col2, dec_col2])
            if len(chunk) == 0:
                print(f"Chunk {i+1} empty after NaN removal.")
                continue
            chunk_filtered = chunk[
                (chunk[ra_col2] >= min_ra) & (chunk[ra_col2] <= max_ra) &
                (chunk[dec_col2] >= min_dec) & (chunk[dec_col2] <= max_dec)
            ]
            if len(chunk_filtered) == 0:
                print(f"Chunk {i+1} has no rows within RA/Dec bounds.")
                continue
            _, matched_df2 = cross_match(df1, chunk_filtered, ra_col1, dec_col1, ra_col2, dec_col2, max_dist_arcsec)
            if len(matched_df2) > 0:
                matched_df2_list.append(matched_df2[columns_to_keep])
        matched_df2 = pd.concat(matched_df2_list, ignore_index=True) if matched_df2_list else pd.DataFrame()
        print(f"Total matches from chunks: {len(matched_df2)}")
        return df1, matched_df2
    except Exception as e:
        print(f"Error in cross_match_in_chunks: {e}")
        raise

# Preprocess 2MASS if needed
def preprocess_2mass(filepath):
    df_2mass = pd.read_csv(filepath)
    print("Original 2MASS dtypes:", df_2mass[['RAJ2000', 'DEJ2000']].dtypes)
    print("Original 2MASS sample:\n", df_2mass[['RAJ2000', 'DEJ2000']].head())
    df_2mass = df_2mass[df_2mass['Qflg'] == 'AAA'].copy()
    print(f"Rows after Qflg filter: {len(df_2mass)}")
    if df_2mass['RAJ2000'].dtype == object or df_2mass['DEJ2000'].dtype == object:
        try:
            coords = SkyCoord(df_2mass['RAJ2000'], df_2mass['DEJ2000'], unit=(u.hourangle, u.deg))
            df_2mass['RAJ2000'] = coords.ra.deg
            df_2mass['DEJ2000'] = coords.dec.deg
            print("Converted 2MASS to decimal degrees.")
        except ValueError as e:
            print(f"Error parsing coordinates: {e}")
            df_2mass = df_2mass.dropna(subset=['RAJ2000', 'DEJ2000'])
            coords = SkyCoord(df_2mass['RAJ2000'], df_2mass['DEJ2000'], unit=(u.hourangle, u.deg))
            df_2mass['RAJ2000'] = coords.ra.deg
            df_2mass['DEJ2000'] = coords.dec.deg
            print("Dropped invalid rows and converted to decimal degrees.")
    else:
        print("RAJ2000 and DEJ2000 are already numeric.")
    # Ensure numeric dtype
    df_2mass['RAJ2000'] = pd.to_numeric(df_2mass['RAJ2000'], errors='coerce')
    df_2mass['DEJ2000'] = pd.to_numeric(df_2mass['DEJ2000'], errors='coerce')
    df_2mass = df_2mass.dropna(subset=['RAJ2000', 'DEJ2000'])
    print("Final 2MASS dtypes:", df_2mass[['RAJ2000', 'DEJ2000']].dtypes)
    print("Final 2MASS sample:\n", df_2mass[['RAJ2000', 'DEJ2000']].head())
    df_2mass.to_csv("2Mass_cleaned.csv", index=False)
    print("Saved cleaned 2MASS to 2Mass_cleaned.csv")
    return "2Mass_cleaned.csv"

# Cross-matching with VizieR catalogues
df_original = df.copy()
print(f"Starting rows in df_original: {len(df_original)}")

# SDSS merged dataset (V/147 + V/154)
sdss_columns = ['zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']
df_matched, sdss_matched = cross_match(df, sdss_merged, 'objra_y', 'objdec', 'RA_ICRS', 'DE_ICRS', max_dist_arcsec=10.0)
print(f"SDSS matches found: {len(df_matched)} galaxies")
df = df_original.merge(
    sdss_matched[sdss_columns + ['RA_ICRS', 'DE_ICRS']], 
    left_on=['objra_y', 'objdec'], 
    right_on=['RA_ICRS', 'DE_ICRS'], 
    how='left'
)
df.drop(columns=['RA_ICRS', 'DE_ICRS'], inplace=True, errors='ignore')
if len(df_matched) == 0:
    print("No matches found with SDSS merged data (V/147 + V/154). Using nsa_z for redshift.")
    df['zsp'] = df['nsa_z']
else:
    print(f"SDSS NaN counts before filling:\n{df[sdss_columns].isna().sum()}")
    df[sdss_columns] = df[sdss_columns].fillna(df[sdss_columns].median(skipna=True))
    print(f"SDSS NaN counts after filling:\n{df[sdss_columns].isna().sum()}")
print(f"Rows after SDSS merge: {len(df)}")

# II/246: 2MASS Extended Source Catalogue
twomass_columns = ['Jmag', 'Hmag', 'Kmag', 'e_Jmag', 'e_Hmag', 'e_Kmag']
print("Starting 2MASS cross-match...")
twomass_file = preprocess_2mass("2Mass.csv")
df_matched, twomass_matched = cross_match_in_chunks(
    df, twomass_file, 'objra_y', 'objdec', 'RAJ2000', 'DEJ2000', twomass_columns, max_dist_arcsec=10.0, chunksize=100000
)
print(f"2MASS matches found: {len(df_matched)} galaxies")
df = df.merge(
    twomass_matched[twomass_columns + ['RAJ2000', 'DEJ2000']], 
    left_on=['objra_y', 'objdec'], 
    right_on=['RAJ2000', 'DEJ2000'], 
    how='left'
)
df.drop(columns=['RAJ2000', 'DEJ2000'], inplace=True, errors='ignore')
if len(df_matched) > 0:
    print(f"2MASS NaN counts before filling:\n{df[twomass_columns].isna().sum()}")
    df[twomass_columns] = df[twomass_columns].fillna(df[twomass_columns].median(skipna=True))
    print(f"2MASS NaN counts after filling:\n{df[twomass_columns].isna().sum()}")
print(f"Rows after 2MASS merge: {len(df)}")

# II/356: GAMA DR3
gama_columns = ['UmAB', 'BmAB', 'VmAB']
print("Starting GAMA DR3 cross-match...")
df_matched, gama_matched = cross_match_in_chunks(
    df, "II356xmmom41s.csv", 'objra_y', 'objdec', 'RAJ2000', 'DEJ2000', gama_columns, max_dist_arcsec=10.0, chunksize=100000
)
print(f"GAMA matches found: {len(df_matched)} galaxies")
df = df.merge(
    gama_matched[gama_columns + ['RAJ2000', 'DEJ2000']], 
    left_on=['objra_y', 'objdec'], 
    right_on=['RAJ2000', 'DEJ2000'], 
    how='left'
)
df.drop(columns=['RAJ2000', 'DEJ2000'], inplace=True, errors='ignore')
if len(df_matched) > 0 and all(col in gama_matched.columns for col in gama_columns):
    print(f"GAMA NaN counts before filling:\n{df[gama_columns].isna().sum()}")
    df[gama_columns] = df[gama_columns].fillna(df[gama_columns].median(skipna=True))
    print(f"GAMA NaN counts after filling:\n{df[gama_columns].isna().sum()}")
else:
    print("No matches found for GAMA DR3 or columns missing, skipping GAMA imputation.")
print(f"Rows after GAMA merge: {len(df)}")
print("Columns in df after cross-matching:", df.columns.tolist())

# SFR calculation
Ha_Hb_intrinsic = 2.86
k_Ha = 2.468
k_Hb = 3.634
H0 = 70  # km/s/Mpc
c = 3e5  # km/s
df['flux_Ha'] = df['F_Ha_cen']
df['e_flux_Ha'] = df['e_F_Ha_cen']
df['flux_Hb'] = df['flux_Hbeta4861.36_Re_fit']
df['flux_OIII_5007'] = df['flux_[OIII]5006.84_Re_fit']
df['flux_NII_6584'] = df['flux_[NII]6583.45_Re_fit']
flux_cols = ['flux_Ha', 'flux_Hb', 'flux_OIII_5007', 'flux_NII_6584', 'e_flux_Ha']
for col in flux_cols:
    df[col] = df[col].replace([np.inf, -np.inf], np.nan).fillna(df[col].median(skipna=True))
df['Ha_Hb_observed'] = df['flux_Ha'] / df['flux_Hb']
df['Ha_Hb_observed'] = df['Ha_Hb_observed'].replace([np.inf, -np.inf], np.nan).fillna(Ha_Hb_intrinsic)
df['A_Ha'] = 2.5 * np.log10(df['Ha_Hb_observed'] / Ha_Hb_intrinsic) * (k_Ha / (k_Hb - k_Ha))
df['A_Ha'] = df['A_Ha'].replace([np.inf, -np.inf], np.nan).fillna(0)
df['flux_Ha_corr'] = df['flux_Ha'] * 10**(0.4 * df['A_Ha'])
df['zsp'] = df['zsp'].replace([np.inf, -np.inf], np.nan).fillna(df['zsp'].median(skipna=True))
df['DL'] = (c * df['zsp'] / H0) * 3.0856e24
df['L_Ha'] = df['flux_Ha_corr'] * 4 * np.pi * df['DL']**2
df['log_SFR_Ha_raw'] = np.log10(df['L_Ha'] * 7.9e-42 + 1e-10)
print(f"Rows after SFR calc: {len(df)}, NaN in log_SFR_Ha_raw: {df['log_SFR_Ha_raw'].isna().sum()}")

# Add raw fluxes and photometric colors
df['log_flux_Ha'] = np.log10(df['flux_Ha'] + 1e-10)
df['log_flux_Hb'] = np.log10(df['flux_Hb'] + 1e-10)
df['log_flux_OIII_5007'] = np.log10(df['flux_OIII_5007'] + 1e-10)
df['log_flux_NII_6584'] = np.log10(df['flux_NII_6584'] + 1e-10)
df['log_e_flux_Ha'] = np.log10(df['e_flux_Ha'] + 1e-10)
if all(col in df.columns for col in ['umag', 'gmag', 'rmag', 'imag', 'zmag']):
    df['color_ug'] = df['umag'] - df['gmag']
    df['color_gr'] = df['gmag'] - df['rmag']
    df['color_ri'] = df['rmag'] - df['imag']
    df['color_iz'] = df['imag'] - df['zmag']
    df['e_color_ug'] = np.sqrt(df['e_umag']**2 + df['e_gmag']**2)
    df['e_color_gr'] = np.sqrt(df['e_gmag']**2 + df['e_rmag']**2)
if all(col in df.columns for col in ['Jmag', 'Kmag']):
    df['color_JK'] = df['Jmag'] - df['Kmag']
    df['e_color_JK'] = np.sqrt(df['e_Jmag']**2 + df['e_Kmag']**2)

# Cosmo-Rank and L_cosmo(s)
gz_df = df.copy()
morph_cols = ['P(CD)', 'P(E)', 'P(S0)', 'P(Sa)', 'P(Sab)', 'P(Sb)', 'P(Sbc)', 'P(Sc)', 'P(Scd)', 'P(Sd)', 'P(Sdm)', 'P(Sm)', 'P(Irr)']
gz_df['morph_sum'] = gz_df[morph_cols].sum(axis=1)
gz_df['Num_w'] = gz_df['conf_prob']
scaler_rank = MinMaxScaler()
gz_df[['morph_sum_norm', 'Num_w_norm', 'nsa_z_norm']] = scaler_rank.fit_transform(gz_df[['morph_sum', 'Num_w', 'nsa_z']])
gz_df['cosmo_rank'] = (0.5 * gz_df['Num_w_norm'] + 0.3 * gz_df['morph_sum_norm'] + 0.2 * gz_df['nsa_z_norm'])
df['cosmo_rank'] = gz_df['cosmo_rank']

alpha = -1.5
M_star = df['log_Mass_gas'].median()
df['a_n'] = (10 ** df['log_Mass_gas'])**(1 + alpha) * np.exp(-10 ** df['log_Mass_gas'] / (10 ** M_star))
bins = pd.qcut(df['Re_kpc'], q=20, labels=False, duplicates='drop') + 1
df['z_bin'] = bins
n_bins = df['z_bin'].nunique()
print(f"Number of unique bins after qcut: {n_bins}")
s_vals = [0.5, 1.0, 1.5, 2.0]
for s in s_vals:
    col_name = f'L_cosmo_s_{s:.1f}'
    df[col_name] = df.groupby('z_bin')['a_n'].transform('mean') / (df['z_bin'] ** s)
df['cosmo_rank_L'] = df['cosmo_rank'] * df['L_cosmo_s_1.0']
df['cosmo_rank_L'] = df['cosmo_rank_L'].replace([np.inf, -np.inf], np.nan).fillna(0)

# Fix plotting to use correct target
plt.scatter(df['L_cosmo_s_1.0'], df['log_SFR_Ha_raw'], alpha=0.5)
plt.xlabel("L_cosmo_s_1.0")
plt.ylabel("log_SFR_Ha_raw")
plt.title("L_cosmo_s_1.0 vs log_SFR_Ha_raw")
plt.savefig("L_cosmo_s1_vs_SFR.png")
plt.close()

# Global imputation before feature engineering
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].replace([np.inf, -np.inf], np.nan).fillna(df[numeric_cols].median(skipna=True))
print(f"Rows after global imputation: {len(df)}")

# Feature engineering
df["mass_metallicity"] = df["log_Mass"] * df["OH_O3N2_cen"]
df["dust_metallicity"] = df["Av_gas_Re"] * df["OH_T04_cen"]
df["disp_mass_ratio"] = df["vel_disp_Ha_cen"] / (df["Sigma_Mass_Re"] + 1e-5)
df["age_metallicity"] = df["Age_LW_Re_fit"] * df["ZH_LW_Re_fit"]
df["sqrt_Re_kpc"] = np.sqrt(df['Re_kpc'] + 1e-5)
df["log_mass"] = np.log(df["log_Mass_gas"] + 1e-5)
df["BSD_likelihood"] = df["log_Mass_gas"] * df["OH_O3N2_cen"] / (df["Av_gas_Re"] + 1e-5 + df["Age_LW_Re_fit"])
df["cosmo_rank_mass"] = df["cosmo_rank"] * df["log_Mass"]
df["L_cosmo_s1_mass"] = df["L_cosmo_s_1.0"] * df["log_Mass"]
df["cosmo_rank_EW"] = df["cosmo_rank"] * df["EW_Ha_cen"]
df["L_cosmo_s1_EW"] = df["L_cosmo_s_1.0"] * df["EW_Ha_cen"]
df["cosmo_rank_scaled"] = df["cosmo_rank"] * 20
df["L_cosmo_s1_scaled"] = df["L_cosmo_s_1.0"] * 20
df["cosmo_rank_L_mass"] = df["cosmo_rank_L"] * df["log_Mass"]
df["L_cosmo_s1_metallicity"] = df["L_cosmo_s_1.0"] * df["OH_O3N2_cen"]

# Define features and target
target = "log_SFR_Ha_raw"
base_features = [
    "log_Mass_gas", "log_Mass", "Av_gas_Re", "Av_ssp_Re", 
    "OH_O3N2_cen", "OH_T04_cen", "OH_dop_cen", "Age_LW_Re_fit", 
    "ZH_LW_Re_fit", "Re_kpc", "vel_disp_Ha_cen", "Lambda_Re", 
    "Sigma_Mass_Re", "EW_Ha_cen", "Ha_Hb_cen"
]
features = base_features + [
    "mass_metallicity", "dust_metallicity", "disp_mass_ratio", 
    "age_metallicity", "sqrt_Re_kpc", "log_mass", "BSD_likelihood", 
    "cosmo_rank", "L_cosmo_s_0.5", "L_cosmo_s_1.5", "L_cosmo_s_2.0", 
    "cosmo_rank_L", "cosmo_rank_mass", "L_cosmo_s1_mass",
    "cosmo_rank_EW", "L_cosmo_s1_EW", "cosmo_rank_scaled", "L_cosmo_s1_scaled",
    "cosmo_rank_L_mass", "L_cosmo_s1_metallicity",
    "log_flux_Ha", "log_flux_Hb", "log_flux_OIII_5007", "log_flux_NII_6584", 
    "log_e_flux_Ha"
]
if 'color_ug' in df.columns:
    features.extend(["color_ug", "color_gr", "color_ri", "color_iz", "e_color_ug", "e_color_gr"])
if 'color_JK' in df.columns:
    features.extend(["color_JK", "e_color_JK"])

# X/y prep
X = df[features]
y = df[target]
X = X.replace([np.inf, -np.inf], np.nan).fillna(X.median(skipna=True))
y = y.replace([np.inf, -np.inf], np.nan).fillna(y.median(skipna=True))
print(f"Rows after X/y prep: {len(X)}, {len(y)}")
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
