import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer


# Define the file path
csv_file = 'Stellar_Mass2_Table_cleaned.csv'


# Load the dataset with error handling
try:
    df = pd.read_csv(csv_file)
    print(f"Successfully loaded '{csv_file}'.")
