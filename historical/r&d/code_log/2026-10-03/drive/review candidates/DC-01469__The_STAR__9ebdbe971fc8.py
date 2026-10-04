# Program imports ========================================================================================================================================================================
import pandas as pd                                                              
import numpy as np                                                            
import shap                                                                    
import matplotlib.pyplot as plt                                                
import seaborn as sns  # Used for correlation heatmap                         
from sklearn.model_selection import train_test_split, cross_val_score, KFold   
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import HistGradientBoostingRegressor
from gplearn.genetic import SymbolicRegressor
import optuna
import warnings
from numpy.polynomial import Polynomial  # Used for SFR trend fitting
from scipy.spatial import cKDTree  # Used for clustering
import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostRegressor
from tqdm import tqdm
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.constants import L_sun
from dustmaps.sfd import SFDQuery                       # Key Notes:
import multiprocessing as mp                        # Confirm all features within csv files 
from functools import partial                      # confirm feature selection section with csv files
import time                                       # confirm L_cosmo(s) and Cosmic Rank features with csv files
import os                                        # complete BSD likeliness section
import pickle                                   # confirm program set for 500,000 rows (down from original 1,000,000 row target)
                                               # Test uses cross matching csv files @ sky cone center coordinates
warnings.filterwarnings("ignore")             # RA 200.0 + DEC 0.0 ~ with a 1 - 6 arcsec cross-match tolerance in a 15 deg. Radius


# List of CSV files  ====================================================================================================================================================================                                                
csv_files = [                            # Survey Table's    
    "ALLWISE_SDSSDR16.csv",            # 1 - ALLWISE + SDSS DR16
    "TwoMass_SDSSDR16.csv",            # 2 - 2Mass + SDSS DR16                
    "STARHORSE2021_SDSSDR16.csv",      # 3 - STARHORSE2021 + SDSS DR16    
    "GALAXGR6+7AIS_SDSSDR16.csv",      # 4 - GALAX GR6+7 AIS + SDSS DR16            
    "UKIDSSDR9LAS_SDSSDR16.csv",       # 5 - UKIDDS DR9 LAS + SDSS DR16    
    "GAIADR3AP_SDSSDR16.csv",          # 6 - GAIA DR3 Astro. Param. + SDSS DR16                     
    "PanST2DR1_SDSSDR16.csv",          # 7 - PanSTARRS-DR1 + SDSS DR16 - (unclear if different than PanSTARRS DR1 table without ("-").)
    "PanSTDR1_SDSSDR16.csv",           # 8 - PanSTARRS DR1 + SDSS DR!6 - (unclear if different than PanSTARRS-DR1 table with ("-").)
    "SDSS_MangaSpec_with_fluxes.csv",  # 9 - SDSS DR16 EmissionLinesPort + MangaSpec    ^^^^^^^^^^^^Program will drop Duplicates^^^^^^^^     
    "merged_galspec_gz2.csv"           # 10 - SDSS DR16 GalSpecExtra + Galaxy Zoo 2
]                                           


# Column mappings for each file =======================================================================================================================================================================
column_mappings = {
    "ALLWISE_SDSSDR16.csv": ['RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 
                             'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag', 'Sp-ID'
    ],# -------------------------------------------------------------------------------------------------------------------------
    "TwoMass_SDSSDR16.csv": ['RA_ICRS', 'DE_ICRS', 'Jmag', 'Kmag', 'e_Jmag', 'e_Kmag', 'Sp-ID'
    ],# -------------------------------------------------------------------------------------------------------------------------
    "STARHORSE2021_SDSSDR16.csv": ['RA_ICRS', 'DE_ICRS', 'mass50', 'AV50', 'met50', 'zsp', 'Sp-ID'
    ],# --------------------------------------------------------------------------------------------------------------------------
    "GALAXGR6+7AIS_SDSSDR16.csv": ['RA_ICRS', 'DE_ICRS', 'Sp-ID'
    ],# ---------------------------------------------------------------------------------------------------------------------------
    "UKIDSSDR9LAS_SDSSDR16.csv": ['RA_ICRS', 'DE_ICRS', 'Sp-ID'
    ],# -----------------------------------------------------------------------------------------------------------------------------
    "GAIADR3AP_SDSSDR16.csv": ['RA_ICRS', 'DE_ICRS', 'A0', 'Age-Flame', 'zsp', 'Sp-ID'
    ],# ----------------------------------------------------------------------------------------------------------------------------
    "PanST2DR1_SDSSDR16.csv": ['RA_ICRS', 'DE_ICRS', 'zsp', 'gmag', 'rmag', 'Sp-ID'
    ],# ------------------------------------------------------------------------------------------------------------------------------
    "PanSTDR1_SDSSDR16.csv": ['RA_ICRS', 'DE_ICRS', 'zsp', 'gmag', 'rmag', 'Sp-ID'
    ],# --------------------------------------------------------------------------------------------------------------------------------
    "SDSS_MangaSpec_with_fluxes.csv": ['SpecObj', 'OH_O3N2_cen', 'OH_T04_cen', 'Av_gas_Re', 'vel_disp_Ha_cen', 
                                       'Sigma_Mass_Re', 'Age_LW_Re_fit', 'ZH_LW_Re_fit', 'EW_Ha_cen', 'stellar_mass', 
                                       'Re_kpc', 'redshift', 'flux_Ha', 'flux_Hb', 'flux_OIII_5007', 'flux_NII_6584', 'e_flux_Ha'
    ],# ----------------------------------------------------------------------------------------------------------------------------------
    "merged_galspec_gz2.csv": ['objid', 'ra', 'dec', 'z', 'logmass', 'petrorad_r', 'ellipticity', 'sfr', 'metallicity'
    ]
}
# Function to standardize RA/Dec and SpecObj
def standardize_columns(df, cols):
    df = df[cols].copy()
    if 'RA_ICRS' in df.columns and 'DE_ICRS' in df.columns:
        df = df.rename(columns={"RA_ICRS": "objra_y", "DE_ICRS": "objdec"})
    if 'Sp-ID' in df.columns:
        df = df.rename(columns={"Sp-ID": "SpecObj"})
        # Handle plate-MJD-fiber format in Sp-ID
        def convert_plate_mjd_fiber(specid):
            try:
                # If specid is already a number, return it
                if isinstance(specid, (int, float)) or (isinstance(specid, str) and specid.replace('.', '').isdigit()):
                    return int(float(specid))
                # Parse plate-MJD-fiber format (e.g., '2689-54149-0290')
                plate, mjd, fiber = map(int, specid.split('-'))
                # Use DR16 SpecObjID formula with a default run2d
                run2d = 26  # Common value for DR16 (e.g., "v5_7_0"); adjust if needed
                specobjid = (plate * 2**40) + (fiber * 2**24) + ((mjd - 50000) * 2**10) + (run2d * 2**2)
                return specobjid
            except (ValueError, AttributeError):
                return pd.NA
        
        # Apply conversion to SpecObj column
        df['SpecObj'] = df['SpecObj'].apply(convert_plate_mjd_fiber)
        # Convert to nullable Int64 type to allow NA values
        df['SpecObj'] = df['SpecObj'].astype('Int64')
        # Log sample SpecObj values
        if not df['SpecObj'].isna().all():
            sample_specobj = df['SpecObj'].dropna().head(5).tolist()
            print(f"Sample SpecObj values in {file}: {sample_specobj}")
    elif 'ra' in df.columns and 'dec' in df.columns:
        df = df.rename(columns={"ra": "objra_y", "dec": "objdec"})
    # Handle SpecObj for SDSS_MangaSpec_with_fluxes.csv
    if 'SpecObj' in df.columns:
        # SpecObj is already in scientific notation (e.g., 2.81E+18)
        df['SpecObj'] = df['SpecObj'].astype('float').astype('Int64')
        # Log sample SpecObj values
        if not df['SpecObj'].isna().all():
            sample_specobj = df['SpecObj'].dropna().head(5).tolist()
            print(f"Sample SpecObj values in {file}: {sample_specobj}")
    return df


# Incremental merge
print("Merging Datasets...")
merged_df = None
for i, file in tqdm(enumerate(csv_files), total=len(csv_files), desc="Merging CSV Files"):
    print(f"Loading {file} ({i+1}/{len(csv_files)})...")
    try:
        chunksize = 50000
        df_chunks = pd.read_csv(file, usecols=column_mappings[file], chunksize=chunksize)
        df = pd.concat([standardize_columns(chunk, column_mappings[file]) for chunk in df_chunks], ignore_index=True)
        print(f"Rows in {file}: {len(df)}, Columns: {len(df.columns)}")
    except ValueError as e:
        print(f"Error loading {file}: {e}. Check column names.")
        continue
    
    # Handle Pan-STARRS
    if file in ["PanST2DR1_SDSSDR16.csv", "PanSTDR1_SDSSDR16.csv"]:
        df['nsa_z'] = df['zsp']
        df['g_r'] = df['gmag'] - df['rmag']
        df['P(E)'] = np.where(df['g_r'] > 0.7, 0.8, 0.2)
        df['P(Sc)'] = np.where(df['g_r'] < 0.5, 0.8, 0.2)
        for morph in ['P(CD)', 'P(S0)', 'P(Sa)', 'P(Sab)', 'P(Sb)', 'P(Sbc)', 'P(Scd)', 'P(Sd)', 'P(Sdm)', 'P(Sm)', 'P(Irr)']:
            df[morph] = 0.1
        df['conf_prob'] = 0.5
    
    if merged_df is None:
        merged_df = df
    else:
        # Default merge keys
        merge_keys = None
        # Prioritize objra_y and objdec if both datasets have them
        if 'objra_y' in df.columns and 'objdec' in df.columns and 'objra_y' in merged_df.columns and 'objdec' in merged_df.columns:
            merge_keys = ['objra_y', 'objdec']
        # Use SpecObj for SDSS_MangaSpec_with_fluxes.csv
        elif file == "SDSS_MangaSpec_with_fluxes.csv" and 'SpecObj' in df.columns and 'SpecObj' in merged_df.columns:
            merge_keys = ['SpecObj']
        # Fall back to objid if available in both datasets
        elif 'objid' in df.columns and 'objid' in merged_df.columns:
            merge_keys = ['objid']
        
        if merge_keys:
            print(f"Merging {file} on {merge_keys}")
            merged_df = merged_df.merge(df, on=merge_keys, how='left', suffixes=('', f'_dup_{i}'))
            dup_cols = [col for col in merged_df.columns if f'_dup_{i}' in col]
            merged_df = merged_df.drop(columns=dup_cols)
        else:
            print(f"Skipping merge for {file}: No common merge keys found")
            continue
    
    if 'objra_y' in merged_df.columns and 'objdec' in merged_df.columns:
        merged_df = merged_df.drop_duplicates(subset=['objra_y', 'objdec'], keep='first')
    elif 'SpecObj' in merged_df.columns:
        merged_df = merged_df.drop_duplicates(subset=['SpecObj'], keep='first')
    print(f"Rows after merging {file}: {len(merged_df)}")
    temp_file = f"temp_merge_step_{i+1}.csv"
    merged_df.to_csv(temp_file, index=False)
    print(f"Saved to {temp_file}")


# Final assignment and save after all merges
df = merged_df
df.to_csv("*STAR_preprocess.csv", index=False)
print(f"Completed merging. Final rows: {len(df)}, columns: {len(df.columns)}. Saved to *STAR_preprocess.csv")
print("Preprocessing completed. Engineering features...")


# Clean metallicity and sfr columns by replacing -9999 with NaN
columns_to_clean = ['metallicity', 'sfr']
