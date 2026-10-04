            tamagawa = prod(E.tamagawa_numbers())
            if is_original:
                tamagawa = 4
            sha_order = 1
            rhs = (omega * reg * sha_order * tamagawa) / (tors_order**2)
            comoving_volume = (omega**2 * reg) * (COSMO_SCALE**3) / 1e9  # Adjusted formula
            print(f"Real period (Omega): {omega} (3-sphere scale factor)")
            print(f"Scaled period (Omega * √κ * COSMO_SCALE): {float(omega * SQRT_KAPPA *
