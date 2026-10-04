import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import shap
from sklearn.impute import SimpleImputer
from scipy.stats import randint


# Step 1: Load the merged dataset
df1 = pd.read_csv('merged_output.csv', low_memory=False)


# Print columns to confirm
print("Columns in merged DataFrame:", df1.columns)


# --- Check for 'fS' flux column and calculate SFR ---
