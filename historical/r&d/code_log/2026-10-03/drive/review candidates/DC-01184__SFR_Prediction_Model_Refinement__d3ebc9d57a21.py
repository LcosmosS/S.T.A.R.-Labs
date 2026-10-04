import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt


# --- Load Datasets --- 
print("Loading datasets...")
df_main = pd.read_csv('/mnt/data/filtered_dataset.csv')  # Replace with the correct path
df_class = pd.read_csv('/mnt/data/GalaxiesClassified.csv')  # Replace with the correct path


# --- Clean and Handle Invalid Variables ---
# We will drop columns from df_class and df_main that are not needed or invalid.
# Check for columns that you want to exclude or clean.


# For example, if you know 'mangaid' is the common column for merging, ensure it's valid.
df_class = df_class[['CATAID', 'RA', 'DEC', 'Z']]  # List only the needed columns from df_class
df_main = df_main[['CATAID', 'log_SFR_Ha', 'log_Mass', 'log_SFR_ssp', 'log_NII_Ha_cen']]  # Example feature columns


# Handle missing values by dropping or filling them, depending on the nature of the data
df_class.dropna(subset=['CATAID'], inplace=True)
df_main.dropna(subset=['CATAID'], inplace=True)


# Merge datasets based on 'CATAID'
df = df_main.merge(df_class, on="CATAID", how="left")
print("Datasets merged.")


# --- Define Features and Target Variable ---
features = [
    'log_SFR_Ha',  # Example feature
