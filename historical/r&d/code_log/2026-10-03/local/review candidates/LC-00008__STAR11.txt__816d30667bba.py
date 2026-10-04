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
import multiprocessing as mp                     # Confirm all features within csv files 
from functools import partial                      # confirm feature selection section with csv files
import time                                               # confirm L_cosmo(s) and Cosmic Rank features with csv files
import os                                                 # complete BSD likeliness section
import pickle                                          # confirm program set for 500,000 rows (down from original 1,000,000 row target)
                                                             # Test uses cross matching csv files @ sky cone center coordinates
warnings.filterwarnings("ignore")        # (RA 200.0 + DEC 0.0 ~ with a 1 - 6 arcsec cross-match tolerance in a 15 deg. Radius )


                                                       
# List of CSV files  ====================================================================================================================================================================                                                
csv_files = [                                                       # Survey Table's
    "ALLWISE_SDSSDR16.csv",                   #1 ALLWISE + SDSS DR16
    "TwoMass_SDSSDR16.csv",                   #2 2Mass + SDSS DR16                
    "STARHORSE2021_SDSSDR16.csv",    #3 STARHORSE2021 + SDSS DR16    
    "GALAXGR6+7AIS_SDSSDR16.csv",     #4 GALAX GR6+7 AIS + SDSS DR16            
    "UKIDSSDR9LAS_SDSSDR16.csv",       #5 UKIDDS DR9 LAS + SDSS DR16    
    "GAIADR3AP_SDSSDR16.csv",              #6 GAIA DR3 Astro. Param. + SDSS DR16              
    "PanST2DR1_SDSSDR16.csv",              #7 PanSTARRS-DR1 + SDSS DR16   
    "PanSTDR1_SDSSDR16.csv",                #8 PanSTARRS DR1 + SDSS DR!6 
    "SDSS_MangaSpec_with_fluxes.csv",     #9 SDSS DR16 + SDSS DR16 EmissionLines + MangaSpecAll     
    "merged_galspec_gz2.csv"                       #10 SDSS DR16 GalSpecAll + Galaxy Zoo 2
]                                           


# Column mappings for each file =======================================================================================================================================================================
column_mappings = {
    "ALLWISE_SDSSDR16.csv": [
        'objID', 'RA_ICRS', 'DE_ICRS', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag',
        'e_rmag', 'e_imag', 'e_zmag', 'Jmag', 'Hmag', 'Kmag', 'e_Jmag', 'e_Hmag', 'e_Kmag', 'zsp'
