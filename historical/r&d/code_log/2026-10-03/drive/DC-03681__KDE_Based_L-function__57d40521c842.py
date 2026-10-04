import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from pysr import PySRRegressor
import optuna
import warnings


warnings.filterwarnings("ignore")


# Load dataset
df = pd.read_csv("merged_data.csv")


# Drop rows with missing target or excessive NaNs
df = df.dropna(subset=["log_SFR_Ha"])
df = df.dropna(axis=0, thresh=int(0.8 * df.shape[1]))
df.fillna(df.median(numeric_only=True), inplace=True)


# Step 1: Cosmo-Rank Construction
# Calculate morph_sum as sum of morphological probabilities
gz_df = df.copy()  # Assuming df includes the Galaxy Zoo features
morph_cols = ['P(CD)', 'P(E)', 'P(S0)', 'P(Sa)', 'P(Sab)', 'P(Sb)', 'P(Sbc)', 
              'P(Sc)', 'P(Scd)', 'P(Sd)', 'P(Sdm)', 'P(Sm)', 'P(Irr)']
gz_df['morph_sum'] = gz_df[morph_cols].sum(axis=1)


# Use conf_prob as Num_w (or replace with actual Num_w if defined differently)
gz_df['Num_w'] = gz_df['conf_prob']


# Normalize morph_sum, Num_w, and nsa_z
scaler_rank = MinMaxScaler()
