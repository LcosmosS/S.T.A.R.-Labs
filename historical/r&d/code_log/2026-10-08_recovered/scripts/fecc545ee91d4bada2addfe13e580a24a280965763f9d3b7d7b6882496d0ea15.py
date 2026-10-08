# confirm.py
import pandas as pd
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
import os

csv_files = [
    "ALLWISE_SDSSDR16.csv", "TwoMass_SDSSDR16.csv", "STARHORSE2021_SDSSDR16.csv",
    "GALAXGR6+7AIS_SDSSDR16.csv", "UKIDSSDR9LAS_SDSSDR16.csv", "GAIADR3AP_SDSSDR16.csv",
    "PanST2DR1_SDSSDR16.csv", "PanSTDR1_SDSSDR16.csv"
]
base_dir = "/home/pmqr7"
center = SkyCoord(ra=185.0*u.deg, dec=32.5*u.deg, frame='icrs')

for file in csv_files:
    file_path = os.path.join(base_dir, file)
    df_sample = pd.read_csv(file_path, nrows=1)
    print(f"\nColumns in {file}: {list(df_sample.columns)}")
    
    # Check coordinates
    df = pd.read_csv(file_path, usecols=['RA_ICRS', 'DE_ICRS'], nrows=10000)
    coords = SkyCoord(ra=df['RA_ICRS'].values*u.deg, dec=df['DE_ICRS'].values*u.deg, frame='icrs')
    sep = coords.separation(center).deg
    print(f"RA range: {df['RA_ICRS'].min():.2f}–{df['RA_ICRS'].max():.2f}")
    print(f"Dec range: {df['DE_ICRS'].min():.2f}–{df['DE_ICRS'].max():.2f}")
    print(f"Max separation: {sep.max():.2f}°, Outside 5°: {(sep > 5).sum()}/{len(df)}")