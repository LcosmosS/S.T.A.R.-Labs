# Calculate median petrorad_r
R0 = df['petrorad_r'].median()


# Define the extended L-function with petrorad_r
def L_cosmo_petrorad(s, M0, R0, df):
    term = (M0 / df['M_i']) * (R0 / df['petrorad_r'])
    return (term ** s).mean()


# Example: Compute L_cosmo(1) with petrorad_r
L_petrorad = L_cosmo_petrorad(1, M0, R0, df)
print(f"Extended L-function with petrorad_r: {L_petrorad:.4f}")
