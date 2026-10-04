import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from scipy.stats import randint, uniform
import matplotlib.pyplot as plt
import psutil  # For monitoring system resources


# Step 1: Monitor System Resources (CPU and Memory)
def check_system_resources():
    memory = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu}%")
    print(f"Memory Usage: {memory.percent}%")
    return cpu, memory.percent


# Step 2: Load the SDSS dataset
df = pd.read_csv('SDSSDR18_200000.csv', low_memory=False)


# Inspect the first few rows of the dataset
print(df.head())


# Step 3: Data Preprocessing
# Handle missing values by imputing with the mean
imputer = SimpleImputer(strategy='mean')
