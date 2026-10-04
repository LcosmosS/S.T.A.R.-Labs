def inverse_b(b, mass, v_disp, r_mpc):
    log_mass = log(mass, 10)
    return b / (2 * log_mass * v_disp / r_mpc)

def star_tuned_offset(rho_star, R=3.383, Omega=0.422, T=1, rank=3):
    Psi_r = rank * (rank + 1) / 2
    return floor(rho_star * (Omega * T**2 * exp(Psi_r / Omega) / R)**rank * exp(-1 / Omega))

# Example: Virgo
b_v = 6320
rho_v = inverse_b(b_v, 1.5e15, 750, 2.2)  # ≈6200