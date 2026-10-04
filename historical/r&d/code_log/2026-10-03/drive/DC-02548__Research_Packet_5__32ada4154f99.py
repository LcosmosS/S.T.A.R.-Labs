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


# Print columns for debugging
print("Columns in merged_data.csv:", df.columns.tolist())
print("Columns in sdss_spec (V/154):", sdss_spec.columns.tolist())
print("Columns in sdss_photo (V/147):", sdss_photo.columns.tolist())
print("Columns in twomass (II/246):", twomass.columns.tolist())
print("Columns in gama (II/356):", gama.columns.tolist())


# Function to clean DataFrame by removing rows with NaN or inf in RA/Dec columns
def clean_coordinates(df, ra_col, dec_col):
    initial_len = len(df)
    # Check for NaN or inf in RA and Dec columns
    mask = (
        df[ra_col].notna() & df[dec_col].notna() &  # Not NaN
        np.isfinite(df[ra_col]) & np.isfinite(df[dec_col])  # Not inf
    )
    df_cleaned = df[mask].copy()
    print(f"Removed {initial_len - len(df_cleaned)} rows from DataFrame due to NaN or inf in {ra_col} or {dec_col}")
    return df_cleaned


# Alternative function to replace NaN with median (commented out)
