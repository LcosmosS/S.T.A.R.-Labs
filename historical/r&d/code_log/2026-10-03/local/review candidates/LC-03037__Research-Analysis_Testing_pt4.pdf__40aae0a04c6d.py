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

            plt.savefig(f"curve_{a}_{b}.png")

            plt.close()

            print(f"Polynomial plot saved as curve_{a}_{b}.png")

        except Exception as e:

            print(f"Failed to generate polynomial plot: {e}")



    print("-" * 20)

    return success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E,
