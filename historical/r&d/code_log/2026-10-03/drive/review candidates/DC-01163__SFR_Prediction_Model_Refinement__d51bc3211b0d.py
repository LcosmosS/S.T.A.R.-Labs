import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import shap
import warnings
warnings.filterwarnings("ignore")


# --- Load and Merge Datasets ---
df_main = pd.read_csv("filtered_dataset.csv")
df_class = pd.read_csv("GalaxiesClassified.csv")
df_mass = pd.read_csv("Stellar_Mass2_Table.csv")
df_hi = pd.read_csv("mangaHIall.csv")


# Example merge strategy (adjust 'CATAID' or other keys as needed)
df = df_main.merge(df_class, on="CATAID", how="left")
df = df.merge(df_mass, on="CATAID", how="left")
df = df.merge(df_hi, on="CATAID", how="left")


# Drop missing values and select features
df.dropna(inplace=True)
target = 'log_SFR_Ha'
