import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt


# Load the CSV file
try:
    df = pd.read_csv('Stellar_Mass2_Table.csv')
    print("Successfully loaded 'Stellar_Mass2_Table.csv'.")
