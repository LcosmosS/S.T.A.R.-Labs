import pandas as pd
import numpy as np


# Define the file path
file_path = 'Stellar_Mass2_Table.csv'


# Load the CSV file into a DataFrame
try:
    df = pd.read_csv(file_path)
