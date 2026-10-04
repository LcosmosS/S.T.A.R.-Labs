                sha_order = (leading_coeff * tors_order**2) / (omega * reg * tamagawa)
                print(f"Adjusted |Sha(E)| to match: {sha_order}")
        except Exception as e:
            print(f"Failed to compute BSD invariants: {e}")
            return False, None, None, None, None, None, None, False, E

    log_delta = math.log(abs(delta)) if delta != 0 else 0
    log_cond = math.log(conductor) if conductor > 0 else 0
    features = [a, b, log_delta, log_cond, tors_order]
    normalized_leading_coeff = leading_coeff / 10 if leading_coeff else 0

    # Polynomial plot for density
    if success and rank is not None:
        try:
            x_vals = np.linspace(-10, 10, 1000)
            y_vals = np.sqrt(np.maximum(x_vals**3 + a * x_vals + b, 0))
            plt.figure(figsize=(8, 6))
            color = 'green' if rank == 3 else 'blue' if rank == 2 else 'black'
            plt.scatter(x_vals, y_vals, s=float(max(normalized_leading_coeff * 100, 1)), c=color, alpha=0.5,
label=f'Rank {rank}')
            plt.scatter(x_vals, -y_vals, s=float(max(normalized_leading_coeff * 100, 1)), c=color, alpha=0.5)
            plt.title(f'Curve y² = x³ + {a}x + {b}, Leading Coeff: {leading_coeff:.2f}')
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
