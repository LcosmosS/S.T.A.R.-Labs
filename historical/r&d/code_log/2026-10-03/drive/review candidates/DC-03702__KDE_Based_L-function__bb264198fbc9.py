import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import psutil
import optuna
from pysr import PySRRegressor
import shap
import warnings


warnings.filterwarnings("ignore")  # Suppress warnings for cleaner output


# -------------------------------
# Helper: System Resource Monitor
def check_system_resources():
    memory = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu}%")
    print(f"Memory Usage: {memory.percent}%")
    return cpu, memory.percent


# -------------------------------
# Step 1: Load the raw GZ dataset (unclean)
gz_df = pd.read_csv("GZ_gzdv1-2_unclean.csv", low_memory=False)
print("Columns in raw GZ DataFrame:", gz_df.columns.tolist())
print(gz_df.head())


# -------------------------------
# Step 2: Automated Data Cleaning
# Convert all numeric columns to numeric type (coerce errors to NaN)
for col in gz_df.columns:
    # Try to convert to numeric if possible; ignore non-numeric columns
    gz_df[col] = pd.to_numeric(gz_df[col], errors='ignore')


# Replace infinite values with NaN and then drop rows that have NaNs in key columns
numeric_cols = gz_df.select_dtypes(include=[np.number]).columns
gz_df[numeric_cols] = gz_df[numeric_cols].replace([np.inf, -np.inf], np.nan)
# Drop rows that have NaNs in the critical columns we need for modeling.
critical_cols = ['z', 'rMag', 'Ar', 'Pth100', 'Smooth', 'Featured']
gz_df.dropna(subset=critical_cols, inplace=True)


# Optionally, you can fill remaining missing values in numeric columns with the mean.
imputer_all = SimpleImputer(strategy='mean')
gz_df[numeric_cols] = imputer_all.fit_transform(gz_df[numeric_cols])


# -------------------------------
# Step 3: Select and preprocess relevant features
selected_features = ['z', 'rMag', 'Ar', 'Pth100', 'Smooth', 'Featured']
gz_df = gz_df[selected_features].copy()


# -------------------------------
# Step 4: Feature Engineering
# Create a morphology feature by summing Smooth and Featured
gz_df['morph_sum'] = gz_df[['Smooth', 'Featured']].sum(axis=1)
# Compute dust-corrected magnitude
gz_df['dust_corrected_mag'] = gz_df['rMag'] - gz_df['Ar']


# Normalize morph_sum and Pth100 for a cosmological rank
scaler_norm = MinMaxScaler()
