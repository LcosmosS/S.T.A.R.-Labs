import pandas as pd
import numpy as np
from scipy.stats import kstest
import matplotlib.pyplot as plt


# Load the dataset (assuming 'Stellar_Mass2_Table.csv' is in the current directory)
try:
    df = pd.read_csv('Stellar_Mass2_Table.csv')
    print("Successfully loaded 'Stellar_Mass2_Table.csv'.")
