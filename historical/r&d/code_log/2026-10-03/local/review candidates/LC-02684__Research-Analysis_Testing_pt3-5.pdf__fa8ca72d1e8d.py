            plt.figure(figsize=(8, 6))
            color = 'green' if rank == 3 else 'blue' if rank == 2 else 'black'
            plt.scatter(x_vals, y_vals, s=float(max(density_size, 1)), c=color, alpha=0.5, label=f'Rank {rank}')
            plt.scatter(x_vals, -y_vals, s=float(max(density_size, 1)), c=color, alpha=0.5)
            # Add regulator contour
            if rank > 0:
                contour_y = np.full_like(x_vals, float(scaled_reg / 1000))
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
    return success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E

# Initialize data
X_data = []
y_data = []
classifier = None
interweb_data = []
seen_pairs = {}

# Main loop
max_successful_curves = 30
max_total_attempts = 70
n = 25
require_3selmer = False
successful_curves = 0
attempts = 0
fib_numbers = generate_fibonacci(n)
print(f"Fibonacci numbers up to index {n}: {fib_numbers}")

with open("interweb_nodes.txt", "w") as f:

f.write("a,b,rank,normalized_leading_coeff,omega,regulator,tamagawa,weak_bsd_holds,log_delta,log_co
