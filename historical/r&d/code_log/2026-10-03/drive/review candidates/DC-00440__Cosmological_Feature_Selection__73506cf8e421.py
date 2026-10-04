import zipfile
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
import optuna
import warnings
from numpy.polynomial import Polynomial


warnings.filterwarnings("ignore")


# Step 1: Extract the CSV from the zip file
zip_file_name = 'data.zip'  # Replace with your actual zip file name
csv_file_name = 'PhotoObj_pmqr771.csv'  # Replace with your actual CSV file name


with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
    zip_ref.extract(csv_file_name)


# Step 2: Load the extracted dataset
df = pd.read_csv(csv_file_name)


# Drop rows with missing target or excessive NaNs
df = df.dropna(subset=["t01_smooth_or_features_a01_smooth_fraction"])
df = df.dropna(axis=0, thresh=int(0.8 * df.shape[1]))
df.fillna(df.median(numeric_only=True), inplace=True)


# Step 3: Cosmo-Rank Construction
gz_df = df.copy()


# Define morphological columns for morph_sum (assuming these are present)
morph_cols = [
    "t01_smooth_or_features_a01_smooth_fraction",
    "t01_smooth_or_features_a02_features_or_disk_fraction",
    "t02_edgeon_a01_yes_fraction",
    "t03_bar_a01_bar_fraction",
    "t04_spiral_a01_spiral_fraction",
    "t05_bulge_prominence_a01_no_bulge_fraction",
    "t06_odd_a01_yes_fraction",
    "t07_rounded_a01_completely_round_fraction",
    "t08_odd_feature_a01_ring_fraction",
    "t09_bulge_shape_a01_rounded_fraction",
    "t10_arms_winding_a01_tight_fraction",
    "t11_arms_number_a01_1_fraction",
    "t12_clumpy_a01_yes_fraction",
    "t13_bright_clump_a01_yes_fraction",
    "t14_bright_clump_central_a01_yes_fraction",
    "t15_clumps_arrangement_a01_line_fraction",
    "t16_clumps_count_a01_1_fraction",
    "t17_clumps_symmetrical_a01_yes_fraction",
    "t18_clumps_embedded_a01_yes_fraction"
]


# Check if morph_cols exist; if not, adjust below
