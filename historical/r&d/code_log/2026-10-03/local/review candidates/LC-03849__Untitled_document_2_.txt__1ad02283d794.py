import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, KFold, cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import joblib


# --- 1. Data Preparation ---
# Load the dataset
df = pd.read_csv('SDSSDR19_200000.csv')
print(f"Dataset loaded with {df.shape[0]} rows and {df.shape[1]} columns.")


# Derive necessary features
# Compute colors
df['g_r'] = df['g'] - df['r']


# Approximate absolute magnitude (r-band) using redshift
# Distance modulus: DM = 5 * log10(d_L/10 pc), d_L ~ (c/H0) * z for small z
H0 = 70  # Hubble constant in km/s/Mpc
c = 3e5  # Speed of light in km/s
df['d_L'] = (c / H0) * df['redshift']  # Luminosity distance in Mpc
df['d_L'] = df['d_L'].replace(0, 1e-6)  # Avoid division by zero
df['dist_mod'] = 5 * np.log10(df['d_L'] * 1e6 / 10)  # Distance modulus
df['M_r'] = df['r'] - df['dist_mod']  # Absolute magnitude


# Estimate stellar mass (nsa_mstar) using a simplified color-magnitude relation
# log(M*) ~ -0.4 * (M_r - M_sun,r) + 0.4 * (g - r) + constant
M_sun_r = 4.64  # Absolute magnitude of the Sun in r-band
df['log_nsa_mstar'] = -0.4 * (df['M_r'] - M_sun_r) + 0.4 * df['g_r'] + 8.0  # Offset for scaling


# Estimate SFR using u-band magnitude as a proxy
df['log_SFR_Ha'] = -0.4 * df['u'] + 2.0  # Simplified proxy (adjust constant as needed)


# Estimate gas mass (log_Mass_gas) using SFR
df['log_Mass_gas'] = df['log_SFR_Ha'] + 8.0  # Simplified relation


# Approximate log_Mass (total mass) as log(nsa_mstar)
df['log_Mass'] = df['log_nsa_mstar']


# Approximate metallicity (OH_Mar13_N2_Re_fit) using mass-metallicity relation
df['OH_Mar13_N2_Re_fit'] = 8.9 - 0.5 * (df['log_nsa_mstar'] - 10)  # Simplified relation


# Approximate dust attenuation (Av_gas_Re) using g-r color
df['Av_gas_Re'] = 1.5 * df['g_r']  # Simplified proxy


# Define desired features
desired_features = [
    'log_Mass_gas', 'log_nsa_mstar', 'log_Mass', 'OH_Mar13_N2_Re_fit', 'Av_gas_Re'
]


# Since all desired features are derived, they should be available
