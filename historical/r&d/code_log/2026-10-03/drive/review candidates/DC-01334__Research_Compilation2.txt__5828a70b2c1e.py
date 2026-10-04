# Function to compute K for a subset
def compute_K(df_subset, M0):
    L_value = (M0 / df_subset['M_i']).mean()  # L_cosmo(1)
    Reg_value = (df_subset['M_i'] / M0).mean()  # Reg_cosmo
    K = Reg_value / L_value
    return K


# Filter high and low SFR groups
median_sfr = df_sfr['sfr'].median()
high_sfr = df_sfr[df_sfr['sfr'] > median_sfr]
low_sfr = df_sfr[df_sfr['sfr'] <= median_sfr]


# Compute K for high SFR group
K_high_sfr = compute_K(high_sfr, M0)
print(f"K for high SFR group: {K_high_sfr:.4f}")


# Compute K for low SFR group
K_low_sfr = compute_K(low_sfr, M0)
print(f"K for low SFR group: {K_low_sfr:.4f}")
