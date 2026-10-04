training_labels = [3, 3, 3, 3, 3]
print(f"Corrected training data: {training_data}")
print(f"Corrected labels: {training_labels}")

# We already have 5 curves, but let's continue to find more for a better dataset
target_3selmer_curves = 7  # Aim for 7 curves to improve the classifier
max_attempts = 100  # Maximum additional attempts
attempt = 71  # Continue from Attempt 71
current_fib_index = 61  # Start extending from index 61

# Continuous testing loop with refined golden ratio scaling
phi_powers = [0, 1, 2]  # Test scaling by φ^0, φ^1, φ^2
while len(training_data) < target_3selmer_curves and attempt <= 70 + max_attempts:
    # Extend Fibonacci sequence if needed
    if current_fib_index >= len(fib_numbers):
        fib_numbers.append(fib_numbers[-1] + fib_numbers[-2])
        print(f"Extended Fibonacci numbers to index {current_fib_index}: {fib_numbers[-1]}")
    current_fib_index += 1

    # Select a and b indices, pairing smaller and larger Fibonacci numbers
    a_idx = (attempt - 71) % 20  # Use smaller Fibonacci numbers (indices 0 to 19)
    b_idx = (attempt - 71) % len(fib_numbers)  # Use larger Fibonacci numbers
    fib_a = fib_numbers[a_idx]
    fib_b = fib_numbers[b_idx]
