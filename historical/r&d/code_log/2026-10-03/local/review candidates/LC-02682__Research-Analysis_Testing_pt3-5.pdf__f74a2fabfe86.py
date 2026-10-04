            print(f"Real period (Omega): {omega} (3-sphere scale factor)")
            print(f"Dynamic COSMO_SCALE: {cosmo_scale}")
            print(f"Scaled period: {float(scaled_period)} light-years")
            print(f"Regulator: {reg} (node interaction strength)")
            print(f"Scaled regulator (Reg * √κ * {'20' if rank == 3 else '12' if rank == 2 else '15' if rank == 1 else
'20'}): {float(scaled_reg)} (density height)")
            print(f"Product of Tamagawa numbers: {tamagawa} (local edge constraints)")
            print(f"Estimated comoving volume (Omega * Reg * scale^3 / {'5e13' if rank == 3 else '1e14'}):
