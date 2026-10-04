import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns


# --- Load and Prepare Data ---
df = pd.read_csv("your_dataset.csv")  # replace with your file path


# Replace -9999 with NaN
df[['OH_Mar13_N2_Re_fit', 'Av_gas_Re']] = df[['OH_Mar13_N2_Re_fit', 'Av_gas_Re']].replace(-9999, np.nan)


# Filter valid data (e.g., QCFLAG == 1)
df = df[df['QCFLAG'] == 1]


# Median Imputation
imputer = SimpleImputer(strategy='median')
