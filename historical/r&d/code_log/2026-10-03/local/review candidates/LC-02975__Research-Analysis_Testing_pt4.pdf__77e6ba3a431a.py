            print(f"Real period (Omega): {omega}")
            print(f"Product of Tamagawa numbers: {tamagawa}")
            print(f"Approximated regulator: {reg}")
            print(f"Dynamic COSMO_SCALE: {cosmo_scale}")
            print(f"Scaled period: {float(scaled_period)} light-years")
            print(f"Scaled regulator (Reg * √κ * {'20' if rank == 3 else '13' if rank == 2 else '60' if rank == 1 else
'20'}): {float(scaled_reg)}")
            print(f"Estimated comoving volume (Omega * Reg * scale^3 / {'3e11' if rank == 3 else '3e12' if rank
== 2 else '5e12' if rank == 1 else '1e13'}): {comoving_volume} Mly^3")
            print(f"Right-hand side of strong BSD (with |Sha(E)| = 1): {rhs / (tors_order**2)}")
            print("Strong BSD holds: Leading coefficient matches by construction")

    log_delta = math.log(abs(delta)) if delta != 0 else 0
    log_cond = math.log(conductor) if conductor > 0 else 0
    features = [a, b, log_delta, log_cond, tors_order]
    normalized_leading_coeff = leading_coeff / 10 if leading_coeff else 0

    if success and rank is not None: