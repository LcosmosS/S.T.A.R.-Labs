import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor


# File path
csv_file = 'Stellar_Mass2_Table_cleaned.csv'


# Load dataset with error handling
try:
    df = pd.read_csv(csv_file)
    print(f"Loaded '{csv_file}' successfully.")
