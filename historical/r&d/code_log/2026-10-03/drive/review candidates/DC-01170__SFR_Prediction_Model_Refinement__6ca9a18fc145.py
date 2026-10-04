import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap


from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


# Load datasets
df_main = pd.read_csv("filtered_dataset.csv")
df_class = pd.read_csv("GalaxiesClassified.csv")
df_mass = pd.read_csv("Stellar_Mass2_Table.csv")
df_hi = pd.read_csv("mangaHIall.csv")


# Normalize column names to lowercase
df_main.columns = df_main.columns.str.lower()
df_class.columns = df_class.columns.str.lower()
df_mass.columns = df_mass.columns.str.lower()
df_hi.columns = df_hi.columns.str.lower()


# Merge all datasets on 'mangaid'
df = df_main.merge(df_class, on="mangaid", how="left")
df = df.merge(df_mass, on="mangaid", how="left")
df = df.merge(df_hi, on="mangaid", how="left")


# Drop rows with missing values
df.dropna(inplace=True)


# Select features and target
target = "sfr"
