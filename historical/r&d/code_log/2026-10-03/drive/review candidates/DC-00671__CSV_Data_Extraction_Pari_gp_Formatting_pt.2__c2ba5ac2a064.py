import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


# Step 1: Load and Preprocess Data
csv_file = 'Stellar_Mass2_Table_cleaned.csv'  # Replace with your dataset path
try:
    df = pd.read_csv(csv_file)
    print(f"Loaded '{csv_file}' successfully.")
