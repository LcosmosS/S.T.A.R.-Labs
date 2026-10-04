import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import shap
from sklearn.impute import SimpleImputer
from scipy.stats import randint
import matplotlib.pyplot as plt


# Step 1: Load the MagPhys dataset
df = pd.read_csv('path_to_magphys_dataset.csv', low_memory=False)


# Print columns to confirm
print("Columns in the MagPhys DataFrame:", df.columns)


# --- Handle missing values in the dataset ---
# We need to check for missing data and impute or drop the rows accordingly
imputer = SimpleImputer(strategy='mean')  # You can change to 'median' if desired


# Assuming features like 'ra', 'dec', 'redshift', etc. are to be used, we will impute them
