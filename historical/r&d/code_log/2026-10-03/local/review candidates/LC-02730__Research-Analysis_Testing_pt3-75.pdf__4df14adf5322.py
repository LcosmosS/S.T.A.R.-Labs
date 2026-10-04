            comoving_volume = (omega * reg * cosmo_scale**3) / (1.5e13 if rank == 3 else 1.5e14 if rank ==
2 else 8e13 if rank == 1 else 1e14)
            scaled_reg = reg * SQRT_KAPPA * (20 if rank == 3 else 7 if rank == 2 else 5 if rank == 1 else 20)
            print(f"Real period (Omega): {omega} (3-sphere scale factor)")
            print(f"Dynamic COSMO_SCALE: {cosmo_scale}")
            print(f"Scaled period: {float(scaled_period)} light-years")
            print(f"Regulator: {reg} (node interaction strength)")
            print(f"Scaled regulator (Reg * √κ * {'20' if rank == 3 else '7' if rank == 2 else '5' if rank == 1 else
'20'}): {float(scaled_reg)} (density height)")
            print(f"Product of Tamagawa numbers: {tamagawa} (local edge constraints)")
            print(f"Estimated comoving volume (Omega * Reg * scale^3 / {'1.5e13' if rank == 3 else '1.5e14' if
rank == 2 else '8e13' if rank == 1 else '1e14'}): {comoving_volume} Mly^3")
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
            y_vals = np.sqrt(np.maximum(x_vals**3 + a * x_vals + b, 0))
            density_size = min(leading_coeff * 177 / 40, 100) if leading_coeff else 10  # Larger rank 3
            plt.figure(figsize=(8, 6))
            color = 'green' if rank == 3 else 'blue' if rank == 2 else 'black'
            plt.scatter(x_vals, y_vals, s=float(max(density_size, 1)), c=color, alpha=0.5, label=f'Rank {rank}')
            plt.scatter(x_vals, -y_vals, s=float(max(density_size, 1)), c=color, alpha=0.5)
            # Fixed regulator contour
            if rank > 0:
                contour_y = np.full_like(x_vals, float(5 if rank == 3 else min(scaled_reg / 800, 4)))
                plt.plot(x_vals, contour_y, 'r--', label=f'Regulator {scaled_reg:.0f}')
                plt.plot(x_vals, -contour_y, 'r--')
            plt.title(f'Curve y² = x³ + {a}x + {b}, Density: {leading_coeff * 177:.0f}')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend()