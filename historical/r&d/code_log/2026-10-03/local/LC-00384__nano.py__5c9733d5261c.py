import pandas as pd
import os

# List your CSV files (adjust as needed)
csv_files = [
    "ALLWISE_SDSSDR16.csv",
    "TwoMass_SDSSDR16.csv",
    "STARHORSE2021_SDSSDR16.csv",
    "GALAXGR6+7AIS_SDSSDR16.csv",
    "UKIDSSDR9LAS_SDSSDR16.csv",
    "GAIADR3AP_SDSSDR16.csv",
    "PanST2DR1_SDSSDR16.csv",
    "PanSTDR1_SDSSDR16.csv"
]

# Directory
base_dir = "/home/pmqr7"

# Check column names
for file in csv_files:
    file_path = os.path.join(base_dir, file)
    if os.path.exists(file_path):
        # Read just the first row to get headers
        df = pd.read_csv(file_path, nrows=1)
        print(f"\nColumns in {file}:")
        print(list(df.columns))
        print(f"Number of columns: {len(df.columns)}")
    else:
        print(f"\n{file} not found in {base_dir}")