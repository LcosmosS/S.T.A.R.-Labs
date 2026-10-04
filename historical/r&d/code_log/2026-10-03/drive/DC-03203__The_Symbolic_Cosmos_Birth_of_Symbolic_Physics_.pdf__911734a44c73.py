# Define the input data for the Virgo Cluster
r_virgo = 54
rho_virgo = 6320
# Define our scaling factor kappa
kappa = 31.59259259259259
# Calculate the coefficients using our provisional projection map
a_calculated = -kappa * r_virgo
b_calculated = rho_virgo
print(f"Calculated a: {a_calculated}")
print(f"Calculated b: {b_calculated}")
