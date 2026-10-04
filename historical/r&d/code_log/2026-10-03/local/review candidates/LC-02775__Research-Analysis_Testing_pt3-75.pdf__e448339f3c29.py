            print(f"Real period (Omega): {omega}")
            print(f"Dynamic COSMO_SCALE: {cosmo_scale}")
            print(f"Scaled period: {float(scaled_period)} light-years")
            print(f"Regulator: {reg}")
            print(f"Scaled regulator (Reg * √κ * {'20' if rank == 3 else '13' if rank == 2 else '10' if rank == 1 else
'20'}): {float(scaled_reg)}")
            print(f"Product of Tamagawa numbers: {tamagawa}")
            print(f"Estimated comoving volume (Omega * Reg * scale^3 / {'1.5e13' if rank == 3 else '5e13' if
rank == 2 else '8e13' if rank == 1 else '1e14'}): {comoving_volume} Mly^3")
            print(f"Right-hand side of strong BSD (with |Sha(E)| = 1): {rhs}")

            if abs(leading_coeff - rhs) < 1e-10:
                print("Strong BSD holds: Leading coefficient matches with |Sha(E)| = 1")
            else:
                sha_order = (leading_coeff * tors_order**2) / (omega * reg * tamagawa)