training_labels = [3, 3, 3, 3, 3]
print(f"Corrected training data: {training_data}")
print(f"Corrected labels: {training_labels}")

# Target 7 curves with 3-Selmer rank >= 3
target_3selmer_curves = 7
max_attempts = 100
attempt = 71
current_fib_index = 62

# Function to compute discriminant
def compute_discriminant(a, b):
    return -16 * (4 * a**3 + 27 * b**2)

# Continuous testing loop with refined golden ratio scaling
phi_powers = [0, 1, 2]
while len(training_data) < target_3selmer_curves and attempt <= 70 + max_attempts:
    # Extend Fibonacci sequence if needed
    if current_fib_index >= len(fib_numbers):
        fib_numbers.append(fib_numbers[-1] + fib_numbers[-2])