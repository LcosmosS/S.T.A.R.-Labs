# STAR: Symbolic, Tuned (Optuna), Astronomy Regressors (Random Forest + Gradient Boosting) # - S: Symbolic Regressor (via gplearn) # - T: Tuned (hyperparameter optimization with Optuna) # - A: Astronomy (predicting star formation rates in galaxies) # - R: Regressors (Random Forest and Gradient Boosting)
import pandas as pd import numpy as np import shap import matplotlib.pyplot as plt import seaborn as sns from sklearn.model_selection import train_test_split, cross_val_score, KFold from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor from sklearn.metrics import r2_score from sklearn.preprocessing import StandardScaler, MinMaxScaler from gplearn.genetic import SymbolicRegressor import optuna import warnings from numpy.polynomial import Polynomial from scipy.spatial import cKDTree import csvwarnings.filterwarnings("ignore")# Load the original dataset df = pd.read_csv("merged_data.csv")# Load the SDSS datasets and merge them sdss_dr16 = pd.read_csv("V154sdss16.csv") # V/154: SDSS DR16 sdss_dr12 = pd.read_csv("V147sdss12.csv") # V/147: SDSS DR12# Merge V/154 and V/147 on objID sdss_merged = pd.merge( sdss_dr16[['objID', 'RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']], sdss_dr12[['objID', 'RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']], on='objID', how='outer', suffixes=('_dr16', '_dr12') )# Combine columns, preferring DR16 values where available, otherwise use DR12 sdss_merged['RA_ICRS'] = sdss_merged['RA_ICRS_dr16'].combine_first(sdss_merged['RA_ICRS_dr12']) sdss_merged['DE_ICRS'] = sdss_merged['DE_ICRS_dr16'].combine_first(sdss_merged['DE_ICRS_dr12']) sdss_merged['zsp'] = sdss_merged['zsp_dr16'].combine_first(sdss_merged['zsp_dr12']) sdss_merged['umag'] = sdss_merged['umag_dr16'].combine_first(sdss_merged['umag_dr12']) sdss_merged['gmag'] = sdss_merged['gmag_dr16'].combine_first(sdss_merged['gmag_dr12']) sdss_merged['rmag'] = sdss_merged['rmag_dr16'].combine_first(sdss_merged['rmag_dr12']) sdss_merged['imag'] = sdss_merged['imag_dr16'].combine_first(sdss_merged['imag_dr12']) sdss_merged['zmag'] = sdss_merged['zmag_dr16'].combine_first(sdss_merged['zmag_dr12']) sdss_merged['e_umag'] = sdss_merged['e_umag_dr16'].combine_first(sdss_merged['e_umag_dr12']) sdss_merged['e_gmag'] = sdss_merged['e_gmag_dr16'].combine_first(sdss_merged['e_gmag_dr12']) sdss_merged['e_rmag'] = sdss_merged['e_rmag_dr16'].combine_first(sdss_merged['e_rmag_dr12']) sdss_merged['e_imag'] = sdss_merged['e_imag_dr16'].combine_first(sdss_merged['e_imag_dr12']) sdss_merged['e_zmag'] = sdss_merged['e_zmag_dr16'].combine_first(sdss_merged['e_zmag_dr12'])# Drop the intermediate columns sdss_merged = sdss_merged[['objID', 'RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']]# Save the merged dataset for future use sdss_merged.to_csv("sdss_merged.csv", index=False) print(f"Merged SDSS dataset created with {len(sdss_merged)} rows.")# Load the other datasets with error handling try: twomass = pd.read_csv("2Mass.csv", on_bad_lines='skip', quoting=csv.QUOTE_ALL) print(f"Loaded 2Mass.csv with {len(twomass)} rows after skipping bad lines.") except Exception as e: print(f"Error loading 2Mass.csv: {e}") print("Attempting to load with a different approach...") with open("2Mass.csv", 'r') as f: lines = f.readlines() header = lines[0].strip().split(',') expected_cols = len(header) cleaned_lines = [lines[0]] for i, line in enumerate(lines[1:], start=1): fields = line.strip().split(',') if len(fields) == expected_cols: cleaned_lines.append(line) else: print(f"Skipped line {i+1} in 2Mass.csv: expected {expected_cols} fields, got {len(fields)}") with open("2Mass_cleaned.csv", 'w') as f: f.writelines(cleaned_lines) twomass = pd.read_csv("2Mass_cleaned.csv") print(f"Loaded cleaned 2Mass.csv with {len(twomass)} rows.")try: gama = pd.read_csv("II356xmmom41s.csv", on_bad_lines='skip', quoting=csv.QUOTE_ALL) print(f"Loaded II356xmmom41s.csv with {len(gama)} rows after skipping bad lines.") except Exception as e: print(f"Error loading II356xmmom41s.csv: {e}") print("Attempting to load with a different approach...") with open("II356xmmom41s.csv", 'r') as f: lines = f.readlines() header = lines[0].strip().split(',') expected_cols = len(header) cleaned_lines = [lines[0]] for i, line in enumerate(lines[1:], start=1): fields = line.strip().split(',') if len(fields) == expected_cols: cleaned_lines.append(line) else: print(f"Skipped line {i+1} in II356xmmom41s.csv: expected {expected_cols} fields, got {len(fields)}") with open("II356xmmom41s_cleaned.csv", 'w') as f: f.writelines(cleaned_lines) gama = pd.read_csv("II356xmmom41s_cleaned.csv") print(f"Loaded cleaned II356xmmom41s.csv with {len(gama)} rows.")# Print columns for debugging print("Columns in merged_data.csv:", df.columns.tolist()) print("Columns in sdss_merged (V/147 + V/154):", sdss_merged.columns.tolist()) print("Columns in twomass (II/246):", twomass.columns.tolist()) print("Columns in gama (II/356):", gama.columns.tolist())# Function to clean DataFrame by removing rows with NaN or inf in RA/Dec columns def clean_coordinates(df, ra_col, dec_col): initial_len = len(df) # Check for NaN or inf in RA and Dec columns mask = ( df[ra_col].notna() & df[dec_col].notna() & # Not NaN np.isfinite(df[ra_col]) & np.isfinite(df[dec_col]) # Not inf ) df_cleaned = df[mask].copy() print(f"Removed {initial_len - len(df_cleaned)} rows from DataFrame due to NaN or inf in {ra_col} or {dec_col}") # Print RA/Dec ranges for debugging if len(df_cleaned) > 0: print(f"RA range in {ra_col}: {df_cleaned[ra_col].min():.4f} to {df_cleaned[ra_col].max():.4f}") print(f"Dec range in {dec_col}: {df_cleaned[dec_col].min():.4f} to {df_cleaned[dec_col].max():.4f}") else: print(f"No valid RA/Dec data after cleaning in {ra_col}/{dec_col}") return df_cleaned# Cross-match function def deg_to_rad(df, ra_col, dec_col): try: df['ra_rad'] = np.radians(df[ra_col]) df['dec_rad'] = np.radians(df[dec_col]) return df except KeyError as e: print(f"KeyError in deg_to_rad: {e}") print(f"Available columns in DataFrame: {df.columns.tolist()}") raisedef cross_match(df1, df2, ra_col1, dec_col1, ra_col2, dec_col2, max_dist_arcsec=10.0): try: # Clean DataFrames to remove rows with NaN or inf in RA/Dec df1_cleaned = clean_coordinates(df1, ra_col1, dec_col1) df2_cleaned = clean_coordinates(df2, ra_col2, dec_col2)
# Check if either DataFrame is empty after cleaning
if len(df1_cleaned) == 0 or len(df2_cleaned) == 0:
    print("One of the DataFrames is empty after cleaning. Cannot perform cross-match.")
    return df1_cleaned, pd.DataFrame()


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


# Print sample matches for debugging
if len(df1_matched) > 0:
    print("Sample matches (first 5):")
    for i in range(min(5, len(df1_matched))):
        print(f"Match {i+1}: {ra_col1}={df1_matched[ra_col1].iloc[i]:.4f}, {dec_col1}={df1_matched[dec_col1].iloc[i]:.4f} "
              f"matched to {ra_col2}={df2_matched[ra_col2].iloc[i]:.4f}, {dec_col2}={df2_matched[dec_col2].iloc[i]:.4f} "
              f"(distance={(dist[matched][i] * 3600 * 180 / np.pi):.2f} arcsec)")
else:
    print("No matches found within the specified radius.")


return df1_matched, df2_matched
