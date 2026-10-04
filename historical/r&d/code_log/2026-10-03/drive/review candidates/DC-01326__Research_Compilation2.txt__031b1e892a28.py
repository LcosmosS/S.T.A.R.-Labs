# Filter out invalid SFR values
df_sfr = df[df['sfr'] != -9999]


# Calculate median SFR
SFR0 = df_sfr['sfr'].median()


# Compute M_i for each galaxy
df_sfr['M_i'] = 10 ** df_sfr['logmass']


# Define the extended L-function with SFR
def L_cosmo_sfr(s, M0, SFR0, df):
    term = (M0 / df['M_i']) * (SFR0 / df['sfr'])
    return (term ** s).mean()


# Example: Compute L_cosmo(1) with SFR
L_sfr = L_cosmo_sfr(1, M0, SFR0, df_sfr)
print(f"Extended L-function with SFR: {L_sfr:.4f}")
