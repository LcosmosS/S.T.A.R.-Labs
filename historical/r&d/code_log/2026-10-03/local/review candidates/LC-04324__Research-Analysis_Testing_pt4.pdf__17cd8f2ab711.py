            print(f"Real period (Omega): {omega}")

            print(f"Dynamic COSMO_SCALE: {cosmo_scale}")
            print(f"Scaled period: {float(scaled_period)} light-years")

            print(f"Regulator: {reg}")

            print(f"Scaled regulator (Reg * √κ * {'20' if rank == 3 else '13' if rank == 2 else '60' if rank == 1 else
'20'}): {float(scaled_reg)}")

            print(f"Product of Tamagawa numbers: {tamagawa}")
