            print(f"Real period (Omega): {omega}")
            print(f"Product of Tamagawa numbers: {tamagawa}")
            print(f"Approximated regulator: {reg}")
            print(f"Dynamic COSMO_SCALE: {cosmo_scale}")
            print(f"Scaled period: {float(scaled_period)} light-years")
            print(f"Scaled regulator (Reg * √κ * {'20' if rank == 3 else '13' if rank == 2 else '60' if rank == 1 else
'20'}): {float(scaled_reg)}")
            print(f"Estimated comoving volume (Omega * Reg * scale^3 / {'3e11' if rank == 3 else '3e12' if rank
== 2 else '5e12' if rank == 1 else '1e13'}): {comoving_volume} Mly^3")