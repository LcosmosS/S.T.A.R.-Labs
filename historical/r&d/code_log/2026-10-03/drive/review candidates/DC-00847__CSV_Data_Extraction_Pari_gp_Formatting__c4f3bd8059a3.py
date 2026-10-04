import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
import os


# Define the path to the CSV file and PARI/GP output file
csv_file = 'Stellar_Mass2_Table.csv'
pari_gp_file = 'C:\\temp\\STM_Extract_Valid.gp'  # Windows-specific path


# Define key columns to process
key_columns = ['ra', 'dec', 'z', 'logmass', 'sfr', 'petrorad_r', 'ellipticity']


try:
    # Load the CSV file
    df = pd.read_csv(csv_file)
