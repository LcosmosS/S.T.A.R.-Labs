    log_mass = log(mass_solar, log_base)
    density_term = v_disp_km_s / r_virial_mpc
    rho = b / (2.0 * log_mass * density_term)
    return round(rho)

# ————————————————————————
# 2. S.T.A.R. Invariant Scaling for Offset
# ————————————————————————
def star_scaled_offset(rho, R=3.383, Omega=0.422, T=1, rank=3):
    """Apply S.T.A.R. ρ_scale to generate recursive offset"""
    Psi_r = rank * (rank + 1) / 2
    scale = (Omega * T**2 * exp(Psi_r / Omega)) / R
    rho_star = rho * (scale**rank) * exp(-1 / Omega)
    return floor(rho_star)

# ————————————————————————
# 3. Cosmic Recurrence with S.T.A.R. Tuning
# ————————————————————————
def star_cosmic_recurrence(distance, rho_star, R=3.383, Omega=0.422, T=1, rank=3):
    """Generate numerators using inverse b + S.T.A.R. invariants"""
    # Define Psi_r inside function (was missing)
    Psi_r = rank * (rank + 1) / 2