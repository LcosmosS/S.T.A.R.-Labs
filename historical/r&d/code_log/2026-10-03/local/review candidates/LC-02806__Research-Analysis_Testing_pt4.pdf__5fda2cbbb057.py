            plt.savefig(f"curve_{a}_{b}.png")
            plt.close()
            print(f"Polynomial plot saved as curve_{a}_{b}.png")
        except Exception as e:
            print(f"Failed to generate polynomial plot: {e}")

    print("-" * 20)
    return success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E

X_data = []
y_data = []
classifier = None
interweb_data = []
seen_pairs = {}
max_successful_curves = 30
max_total_attempts = 35  # Increased to explore more curves
n = 25
require_3selmer = False
successful_curves = 0
attempts = 0
fib_numbers = generate_fibonacci(n)
print(f"Fibonacci numbers up to index {n}: {fib_numbers}")

with open("interweb_nodes.txt", "w") as f:

f.write("a,b,rank,normalized_leading_coeff,omega,regulator,tamagawa,weak_bsd_holds,log_delta,log_co
