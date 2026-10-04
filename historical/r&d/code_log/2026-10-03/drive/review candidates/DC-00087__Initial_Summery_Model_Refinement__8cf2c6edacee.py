import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from pysr import PySRRegressor
import psutil  # For memory monitoring
import warnings


warnings.filterwarnings("ignore")


# Helper: Memory Check
def check_memory():
    memory = psutil.virtual_memory()
    print(f"Memory Usage: {memory.percent}% (Used: {memory.used / 1024**3:.2f} GB, Total: {memory.total / 1024**3:.2f} GB)")
    return memory.percent


# Load dataset
print("Loading data...")
check_memory()
df = pd.read_csv("merged_data.csv")


# Step 1: Data Cleaning
df = df.dropna(subset=["log_SFR_Ha"])  # Drop rows missing target
df = df.dropna(axis=0, thresh=int(0.8 * df.shape[1]))  # Drop rows with >20% NaNs
df.fillna(df.median(numeric_only=True), inplace=True)  # Impute remaining NaNs with median


# Step 2: Cosmo-Rank Construction
morph_cols = ['P(CD)', 'P(E)', 'P(S0)', 'P(Sa)', 'P(Sab)', 'P(Sb)', 'P(Sbc)', 
              'P(Sc)', 'P(Scd)', 'P(Sd)', 'P(Sdm)', 'P(Sm)', 'P(Irr)']
df['morph_sum'] = df[morph_cols].sum(axis=1)
df['Num_w'] = df['conf_prob']  # Confidence proxy


# Normalize for cosmo_rank
scaler_rank = MinMaxScaler()
