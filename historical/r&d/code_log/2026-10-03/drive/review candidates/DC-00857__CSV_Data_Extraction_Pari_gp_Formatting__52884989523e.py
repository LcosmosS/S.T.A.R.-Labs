import pandas as pd import numpy as np from sklearn.mixture import GaussianMixture import os
# Define file paths
csv_file = 'Stellar_Mass2_Table.csv' # Input CSV file pari_gp_file = 'C:\\temp\\STM_Extract_Valid.gp' # Output PARI/GP file (Windows-specific)
# Define key columns to process
key_columns = ['ra', 'dec', 'z', 'logmass', 'sfr', 'petrorad_r', 'ellipticity']
# Step 1: Load the CSV file with error handling
