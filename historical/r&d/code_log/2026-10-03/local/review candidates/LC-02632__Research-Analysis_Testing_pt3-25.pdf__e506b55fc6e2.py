            print(f"Real period (Omega): {omega} (3-sphere scale factor)")
            print(f"Dynamic COSMO_SCALE: {cosmo_scale}")
            print(f"Scaled period: {float(scaled_period)} light-years")
            print(f"Regulator: {reg} (node interaction strength)")
            print(f"Scaled regulator (Reg * √κ * {'15' if rank == 3 else '10' if rank >= 2 else '20'}):
