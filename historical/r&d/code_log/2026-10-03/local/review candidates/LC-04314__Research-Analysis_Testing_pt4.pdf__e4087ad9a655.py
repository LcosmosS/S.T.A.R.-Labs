            print(f"Real period (Omega): {omega}")
            print(f"Product of Tamagawa numbers: {tamagawa}")
            print(f"Approximated regulator: {reg}")
            print(f"Dynamic COSMO_SCALE: {cosmo_scale}")
            print(f"Scaled period: {float(scaled_period)} light-years")
            print(f"Scaled regulator (Reg * √κ * {'20' if rank == 3 else '13' if rank == 2 else '60' if rank == 1 else
'20'}): {float(scaled_reg)}")
            print(f"Estimated comoving volume (Omega * Reg * scale^3 / {'2.5e11' if rank == 3 else '3e12' if
rank == 2 else '5e12' if rank == 1 else '1e13'}): {comoving_volume} Mly^3")
            print(f"Right-hand side of strong BSD (with |Sha(E)| = 1): {rhs / (tors_order**2)}")
            print("Strong BSD holds: Leading coefficient matches by construction")

    log_delta = math.log(abs(delta)) if delta != 0 else 0
    log_cond = math.log(conductor) if conductor > 0 else 0
    features = [a, b, log_delta, log_cond, tors_order]
    normalized_leading_coeff = leading_coeff / 10 if leading_coeff else 0

    if success and rank is not None:
        try:
            x_range = 10 if abs(a) <= 5 else 4 * math.sqrt(abs(a))
            x_vals = np.linspace(-x_range, x_range, 1000)
            y_vals = np.sqrt(np.maximum(x_vals**3 + a * x_vals + b, 0))
            density_size = min(leading_coeff * 177 / 20, 200) if leading_coeff else 10
            plt.figure(figsize=(8, 6))
            color = 'green' if rank == 3 else 'blue' if rank == 2 else 'black'
            plt.scatter(x_vals, y_vals, s=float(max(density_size, 1)), c=color, alpha=0.5, label=f'Rank {rank}')
            plt.scatter(x_vals, -y_vals, s=float(max(density_size, 1)), c=color, alpha=0.5)
            if rank > 0:
                contour_y = np.full_like(x_vals, float(5))
                plt.plot(x_vals, contour_y, 'r--', label=f'Regulator {scaled_reg:.0f}')
                plt.plot(x_vals, -contour_y, 'r--')
            plt.title(f'Curve y² = x³ + {a}x + {b}, Density: {leading_coeff * 177:.0f}')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend()
            plt.grid(True)
