# Cosmological Constants
VIRGO_DISTANCE = 54e6  # 54 million light-years
VIRGO_COMOVING_VOLUME = 1e9  # Mly^3
KAPPA = 1000
SQRT_KAPPA = 31.6227766

# Foundational curve's real period (pre-calculated)
VIRGO_OMEGA = 0.42236

# Define the master scaling constant
COSMO_SCALE = VIRGO_DISTANCE / (VIRGO_OMEGA * SQRT_KAPPA)

# --- Inside the main loop, for a validated curve ---

# Calculate Physical Distance
scaled_period = omega * COSMO_SCALE
print(f"Scaled Period: {scaled_period} light-years")

# Calculate Density Height
# (Scaling factor here can be adjusted based on rank)
scaled_regulator = reg * SQRT_KAPPA * 15
print(f"Scaled Regulator (Density Height): {scaled_regulator}")

# Estimate Comoving Volume
# (Denominator is adjusted based on rank to match observations)
volume_denominator = 1e14
comoving_volume = (omega * reg * COSMO_SCALE**3) / volume_denominator
print(f"Estimated Comoving Volume: {comoving_volume} Mly^3")
