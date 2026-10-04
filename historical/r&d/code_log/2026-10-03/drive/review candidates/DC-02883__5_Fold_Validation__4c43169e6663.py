import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, KFold, cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import joblib


# --- 1. Data Preparation ---
# Load the dataset
df = pd.read_csv('pipe3d_data2.csv')
print(f"Dataset loaded with {df.shape[0]} rows and {df.shape[1]} columns.")


# Define the target variable and the list of desired features
target = 'log_SFR_Ha'  # Assuming this is your target based on context
desired_features = [
    'log_Mass_gas', 'nsa_mstar', 'log_Mass', 'vel_sigma_Re',
    'OH_Mar13_N2_Re_fit', 'Av_gas_Re', 'Age_LW_Re_fit', 'vel_disp_ssp_1Re',
    'L-dust', 'sSfr_0_1Gr', 'mass_dust', 'tau_v', 'mass_stellar'
]


# Identify which desired features are actually in the dataset
