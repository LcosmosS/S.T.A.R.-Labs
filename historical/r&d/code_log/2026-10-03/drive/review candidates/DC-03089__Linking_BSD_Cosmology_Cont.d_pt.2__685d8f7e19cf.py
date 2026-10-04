import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt


# --- Correct Data Path ---
# Adjusted path for WSL; assuming the file is in your home directory
sdss_path = '/home/pmqr7/data/SDSSDR18_Updated.csv'


# --- Load Dataset with Error Handling ---
print("Loading dataset...")
try:
    df = pd.read_csv(sdss_path)
    print(f"Dataset loaded successfully: {sdss_path}")
