    # x-numerator: distance + regulator scaling
    num_x = round(distance * (R**(1/rank) * abs(log(Omega)) / log(3)))

    # y-numerator: recursive multiplier + S.T.A.R. offset
    mult = T**2 * exp(Psi_r / Omega)
    offset = star_scaled_offset(rho_star, R, Omega, T, rank)
    num_y = round(num_x * mult) + offset

    return num_x, num_y

def predict_star_generator(distance, b, mass, v_disp, r_mpc, R=3.383, Omega=0.422, T=1, rank=3):
    """Full inverse pipeline: b → ρ → P"""
    # Step 1: Inverse b → ρ
    rho = inverse_b_to_rho(b, mass, v_disp, r_mpc)

    # Step 2: S.T.A.R. scale ρ → ρ*
    rho_star = rho  # or apply full scaling if needed

    # Step 3: Recurrence
    num_x, num_y = star_cosmic_recurrence(distance, rho_star, R, Omega, T, rank)

    # Step 4: Fixed 3-power denominators
    d_x = 3**4  # 81
    d_y = 3**6  # 729

    return (QQ(num_x)/d_x, QQ(num_y)/d_y, 1), rho

# ————————————————————————
# 4. TEST CORPUS: Known Clusters
# ————————————————————————
clusters = [
    # name, r (MLy), b (from curve), mass (M_sun), v_disp (km/s), r_virial (Mpc)
    ("Virgo",      54,  6200, 1.5e15, 750, 2.2),
    ("Coma",      321, 9980, 2.0e15, 978, 3.0),
