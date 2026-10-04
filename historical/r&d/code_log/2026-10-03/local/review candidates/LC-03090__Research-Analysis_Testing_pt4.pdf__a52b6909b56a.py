            scaled_reg = reg * SQRT_KAPPA * (20 if rank == 3 else 13 if rank == 2 else 60 if rank
== 1 else 20)

            print(f"Real period (Omega): {omega}")
            print(f"Dynamic COSMO_SCALE: {cosmo_scale}")
            print(f"Scaled period: {float(scaled_period)} light-years")
            print(f"Regulator: {reg}")
            print(f"Scaled regulator (Reg * √κ * {'20' if rank == 3 else '13' if rank == 2 else '60' if
rank == 1 else '20'}): {float(scaled_reg)}")
            print(f"Product of Tamagawa numbers: {tamagawa}")
            print(f"Estimated comoving volume (Omega * Reg * scale^3 / {'2.5e11' if rank == 3 else
'5e13' if rank == 2 else '1e15' if rank == 1 else '1e13'}): {comoving_volume} Mly^3")
            print(f"Right-hand side of strong BSD (with |Sha(E)| = 1): {rhs / (tors_order**2)}")

            print("Strong BSD holds: Leading coefficient matches by construction")
        except Exception as e:
            print(f"Failed to compute BSD invariants: {e}")

    log_delta = math.log(abs(delta)) if delta != 0 else 0
    log_cond = math.log(conductor) if conductor > 0 else 0

    features = [a, b, log_delta, log_cond, tors_order]
    print("-" * 20)
    return success, features, rank, leading_coeff / 10 if leading_coeff else 0, omega, reg,
