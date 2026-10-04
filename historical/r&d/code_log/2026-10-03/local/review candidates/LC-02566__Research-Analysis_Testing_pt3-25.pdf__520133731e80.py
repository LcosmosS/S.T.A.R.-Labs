        except:
            print("L-function computation failed")
            return False, None, None, None, None, None, None, False

        try:
            omega = E.period_lattice().real_period(prec=100)
            reg = E.regulator() if rank > 0 else 1.0
            tamagawa = prod(E.tamagawa_numbers())
            if is_original:
                tamagawa = 4
            sha_order = 1
            rhs = (omega * reg * sha_order * tamagawa) / (tors_order**2)
            comoving_volume = (omega**3) * (COSMO_SCALE**3) / 1e9  # Estimate in Mly^3
            print(f"Real period (Omega): {omega} (3-sphere scale factor)")
            print(f"Scaled period (Omega * √κ * COSMO_SCALE): {float(omega * SQRT_KAPPA *
