import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer


# Load dataset
csv_file = 'Stellar_Mass2_Table_cleaned.csv'
try:
    df = pd.read_csv(csv_file)
    print(f"Loaded '{csv_file}' successfully.")
