import pandas as pd
import numpy as np


# Load the synthetic data
df = pd.read_csv("synthetic_cosmic_catalog_calibrated.csv")


# Inspect the first few rows and info
print("Head:")
print(df.head())
print("\nInfo:")
print(df.info())


# Check for duplicates or very close coordinates
coords_cols = ['synthetic_RA', 'synthetic_DE', 'synthetic_z']
print("\nCoordinate Stats:")
print(df[coords_cols].describe())


# Check for duplicates
num_duplicates = df.duplicated(subset=coords_cols).sum()
print(f"\nNumber of duplicate coordinates: {num_duplicates}")
