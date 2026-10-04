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


warnings.filterwarnings("ignore")  # Suppress any future warnings for cleaner output


# -------------------------------
# Helper: System Resource Monitor
def check_system_resources():
    memory = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu}%")
    print(f"Memory Usage: {memory.percent}%")
    return cpu, memory.percent


# -------------------------------
# Step 1: Load the GZ dataset
gz_df = pd.read_csv("GZ_gzdv1-2_cleaned.csv", low_memory=False)
print("Columns in GZ DataFrame:", gz_df.columns.tolist())
print(gz_df.head())


# -------------------------------
# Step 2: Select and preprocess relevant features
selected_features = ['z', 'rMag', 'Ar', 'Pth100', 'Smooth', 'Featured']
gz_df = gz_df[selected_features].copy()


# Impute missing values
gz_df[selected_features] = SimpleImputer(strategy='mean').fit_transform(gz_df[selected_features])


# -------------------------------
# Step 3: Feature Engineering
gz_df['morph_sum'] = gz_df[['Smooth', 'Featured']].sum(axis=1)
gz_df['dust_corrected_mag'] = gz_df['rMag'] - gz_df['Ar']


# Normalize both variables
scaler_norm = MinMaxScaler()
