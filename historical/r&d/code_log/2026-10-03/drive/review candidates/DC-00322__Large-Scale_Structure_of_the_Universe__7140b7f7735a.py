import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from scipy.stats import randint, uniform
import matplotlib.pyplot as plt


# Step 1: Load the SDSS dataset
df = pd.read_csv('SDSSDR18_200000.csv', low_memory=False)


# Inspect the first few rows of the dataset
print(df.head())


# Step 2: Data Preprocessing
# Handle missing values by imputing with the mean
imputer = SimpleImputer(strategy='mean')
