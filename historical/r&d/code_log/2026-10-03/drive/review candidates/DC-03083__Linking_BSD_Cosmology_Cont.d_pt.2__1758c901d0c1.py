import pandas as pd import numpy as np import matplotlib.pyplot as plt from sklearn.model_selection import KFold, cross_val_score, GridSearchCV, train_test_split from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor from sklearn.metrics import mean_squared_error, r2_score import joblib import xgboost as xgb
# Step 1: Load the dataset
df = pd.read_csv('filtered_Pipe3D.csv') # Replace with your dataset file print(f"Dataset loaded with {len(df)} rows and {len(df.columns)} columns.")
# Step 2: Feature Engineering - Add interaction term # Example: Interaction between log_Mass_gas and log_Mass
