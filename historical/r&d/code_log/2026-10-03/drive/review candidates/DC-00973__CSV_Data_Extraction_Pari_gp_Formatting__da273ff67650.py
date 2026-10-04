import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.impute import SimpleImputer
from scipy.stats import kstest, norm
import matplotlib.pyplot as plt
import powerlaw
from sklearn.mixture import GaussianMixture as GMM_bimodal


# Load the data
csv_file = 'Stellar_Mass2_Table.csv'
try:
    df = pd.read_csv(csv_file)
    print(f"Loaded '{csv_file}' successfully.")
