# Define the extended L-function with ellipticity
def L_cosmo_ellipticity(s, M0, df):
    term = (M0 / df['M_i']) * (2.71828 ** (-df['ellipticity']))
    return (term ** s).mean()


# Example: Compute L_cosmo(1) with ellipticity
L_ellipticity = L_cosmo_ellipticity(1, M0, df)
print(f"Extended L-function with ellipticity: {L_ellipticity:.4f}")
