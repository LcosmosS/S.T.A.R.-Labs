            print(f"Real period (Omega): {omega} (3-sphere scale factor)")
            print(f"Dynamic COSMO_SCALE: {cosmo_scale}")
            print(f"Scaled period: {float(scaled_period)} light-years")
            print(f"Regulator: {reg} (node interaction strength)")
            print(f"Scaled regulator (Reg * √κ * {'20' if rank == 3 else '10' if rank == 2 else '7' if rank == 1 else
'20'}): {float(scaled_reg)} (density height)")
            print(f"Product of Tamagawa numbers: {tamagawa} (local edge constraints)")
            print(f"Estimated comoving volume (Omega * Reg * scale^3 / {'1.5e13' if rank == 3 else '1e14' if
rank == 2 else '7e13' if rank == 1 else '1e14'}): {comoving_volume} Mly^3")
            print(f"Right-hand side of strong BSD (with |Sha(E)| = 1): {rhs}")

            if abs(leading_coeff - rhs) < 1e-10:
                print("Strong BSD holds: Leading coefficient matches with |Sha(E)| = 1")
            else:
                print("Strong BSD fails: Leading coefficient does not match with |Sha(E)| = 1")
                sha_order = (leading_coeff * tors_order**2) / (omega * reg * tamagawa)
                print(f"Adjusted |Sha(E)| to match: {sha_order}")
        except Exception as e:
            print(f"Failed to compute BSD invariants: {e}")
            return False, None, None, None, None, None, None, False, E

    log_delta = math.log(abs(delta)) if delta != 0 else 0
    log_cond = math.log(conductor) if conductor > 0 else 0
    features = [a, b, log_delta, log_cond, tors_order]
    normalized_leading_coeff = leading_coeff / 10 if leading_coeff else 0

    # Enhanced polynomial plot
    if success and rank is not None:
        try:
            x_range = 10 if abs(a) <= 5 else 4 * math.sqrt(abs(a))
            x_vals = np.linspace(-x_range, x_range, 1000)