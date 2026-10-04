import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import powerlaw


# 1. Load and Preprocess Data
csv_file = 'Stellar_Mass2_Table.csv'
try:
    df = pd.read_csv(csv_file)
    print(f"Loaded '{csv_file}' successfully.")
