import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import shap


# Step 1: Load the merged DataFrame
df1 = pd.read_csv('merged_output.csv', low_memory=False)


# Print columns to confirm
print("Columns in merged DataFrame:", df1.columns)


# Check if the required columns are present, or if they need to be created/renamed
required_columns = ['log_Mass', 'sfr', 'redshift', 'metallicity', 'ra', 'dec']
