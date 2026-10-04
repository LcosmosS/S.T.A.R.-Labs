    print("Computed cosmo_rank using ellipticity and redshift proxies.")
else:
    print("Warning: ellipticity or redshift missing. Setting cosmo_rank to 0.5.")
    df['cosmo_rank'] = 0.5

# Ensure cosmo_rank is numeric and imputed
========================================================================
======================================================================
df['cosmo_rank'] = pd.to_numeric(df['cosmo_rank'], errors='coerce').replace([np.inf, -np.inf],
np.nan).fillna(0.5)

# Step 2: L_cosmo(s) Construction
========================================================================
========================================================================
=========
if 'logmass' in df.columns:
    df['logMass'] = df['logmass']
if 'petrorad_r' in df.columns:
    df['kronRad'] = df['petrorad_r']

alpha = -1.5
if 'logMass' in df.columns and 'kronRad' in df.columns:
    df['log_Mass_gas'] = df['logMass']
    M_star = df['log_Mass_gas'].median()
    df['a_n'] = (10 ** df['log_Mass_gas'])**(1 + alpha) * np.exp(-10 ** df['log_Mass_gas'] / (10 **
