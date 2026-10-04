import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
from scipy.stats import kstest, norm, gamma
import os


# Define file paths using os.path.join for cross-platform compatibility
csv_file = os.path.join(os.getcwd(), 'Stellar_Mass2_Table.csv')  # Input CSV file
pari_gp_dir = 'temp'  # Directory for PARI/GP file
pari_gp_file = os.path.join(pari_gp_dir, 'STM_Extract_Valid.gp')  # Output PARI/GP file


# Ensure the output directory exists
os.makedirs(pari_gp_dir, exist_ok=True)


# Define key columns to process
key_columns = ['ra', 'dec', 'z', 'logmass', 'sfr', 'petrorad_r', 'ellipticity']


# Step 1: Load the CSV file with error handling
try:
    df = pd.read_csv(csv_file)
    print(f"Successfully loaded '{csv_file}'.")
