import pandas as pd
import numpy as np


# Define the relevant columns (including optional ones)
columns_to_keep = [
    'log_SFR_Ha',  # Target variable
    'log_Mass',
    'nsa_redshift',
    'log_Mass_gas',
    'OH_Mar13_N2_Re_fit',
    'Re_kpc',
    'ellip',
    'vel_disp_ssp_1Re',
    'u-g',
    'g-r',
    'r-i',
    'i-z',
    'nsa_mstar',
    'vel_sigma_Re',
    'V-band_SB_at_Re',
    'Lambda_Re'
]


# Load the dataset
df = pd.read_csv('Pipe3D.csv')
print(f"Initial number of rows: {len(df)}")


# Check if all required columns are present
