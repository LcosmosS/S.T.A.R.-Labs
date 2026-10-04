import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.impute import SimpleImputer
from scipy.stats import kstest, gamma, norm
import matplotlib.pyplot as plt


# Define the file path
csv_file = 'Stellar_Mass2_Table.csv'


# Load the CSV file with error handling
try:
    df = pd.read_csv(csv_file)
    print(f"Successfully loaded '{csv_file}'.")
