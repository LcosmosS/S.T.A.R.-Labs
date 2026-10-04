import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt


# Define file path
csv_file = 'Stellar_Mass2_Table.csv'


# Step 1: Load the CSV file with error handling
try:
    df = pd.read_csv(csv_file)
    print(f"Successfully loaded '{csv_file}'.")
