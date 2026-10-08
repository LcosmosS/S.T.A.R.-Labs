import pandas as pd
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u

# Load a sample of the CSV
try:
    df_test = pd.read_csv("ALLWISE_SDSSDR16.csv", usecols=['RA_ICRS', 'DE_ICRS'], nrows=10000)
except FileNotFoundError:
    print("Error: ALLWISE_SDSSDR16.csv not found in /home/pmqr7")
    exit(1)
except ValueError as e:
    print(f"Error: Invalid columns in CSV: {e}")
    exit(1)

# Validate RA/Dec data
if df_test['RA_ICRS'].isna().sum() > 0 or df_test['DE_ICRS'].isna().sum() > 0:
    print(f"Warning: NaNs detected - RA_ICRS: {df_test['RA_ICRS'].isna().sum()}, DE_ICRS: {df_test['DE_ICRS'].isna().sum()}")
    df_test = df_test.dropna(subset=['RA_ICRS', 'DE_ICRS'])

if not (df_test['RA_ICRS'].dtype in [np.float64, np.float32] and df_test['DE_ICRS'].dtype in [np.float64, np.float32]):
    print("Error: RA_ICRS or DE_ICRS contains non-numeric data")
    exit(1)

if np.any(np.isinf(df_test['RA_ICRS'])) or np.any(np.isinf(df_test['DE_ICRS'])):
    print("Warning: Infinities detected in RA_ICRS or DE_ICRS")
    df_test = df_test[~np.isinf(df_test['RA_ICRS']) & ~np.isinf(df_test['DE_ICRS'])]

if len(df_test) == 0:
    print("Error: No valid rows after cleaning")
    exit(1)

# Compute separations
try:
    coords = SkyCoord(ra=df_test['RA_ICRS']*u.deg, dec=df_test['DE_ICRS']*u.deg, frame='icrs')
    center = SkyCoord(ra=185.0*u.deg, dec=32.5*u.deg, frame='icrs')
    separations = coords.separation(center).deg
    print(f"Rows checked: {len(df_test)}")
    print(f"Max separation: {separations.max():.2f}°")
    print(f"Rows outside 5°: {(separations > 5.0).sum()}")
except ValueError as e:
    print(f"Error in SkyCoord: {e}")
    exit(1)