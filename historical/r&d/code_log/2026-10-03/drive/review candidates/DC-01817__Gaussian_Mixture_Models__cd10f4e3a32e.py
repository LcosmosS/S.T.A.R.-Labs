import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt


# Define file path
file_path = 'Stellar_Mass2_Table.csv'


# Load data into DataFrame 'df'
try:
    df = pd.read_csv(file_path, dtype={'objid': str})
