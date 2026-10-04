import pandas as pd
import numpy as np


# Load the updated dataset
df = pd.read_csv('SDSSDR18_Updated.csv')


# Compute OH_Mar13_N2_Re_fit (metallicity) using N2 method
df['N2'] = np.log10(df['nii_6584_flux'] / df['h_alpha_flux'])
df['OH_Mar13_N2_Re_fit'] = 8.90 + 0.57 * df['N2']


# Compute Av_gas_Re (dust attenuation) using Balmer decrement
df['Ha_Hb'] = df['h_alpha_flux'] / df['h_beta_flux']
df['Av_gas_Re'] = 2.5 * 3.33 * np.log10(df['Ha_Hb'] / 2.86)


# Derive log_Mass_gas (simplified scaling with SFR)
df['log_Mass_gas'] = np.log10(df['sfr']) + 8.0  # Adjust constant as needed


# Compute interaction terms
df['log_Mass_gas_nsa_mstar'] = df['log_Mass_gas'] * df['nsa_mstar']
df['log_Mass_gas_squared'] = df['log_Mass_gas'] ** 2


# Proceed with model training...
