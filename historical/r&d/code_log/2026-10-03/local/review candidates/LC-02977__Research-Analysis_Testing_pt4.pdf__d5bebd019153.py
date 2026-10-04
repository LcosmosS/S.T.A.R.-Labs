# Generate Fibonacci numbers
def generate_fibonacci(n):
    fib = [0, 1]
    for i in range(2, n + 1):
        fib.append(fib[i-1] + fib[i-2])
    return fib

# Initial Fibonacci numbers up to index 43
fib_numbers = generate_fibonacci(43)
print(f"Fibonacci numbers up to index 43: {fib_numbers}")

# Training data for high 3-Selmer ranks
training_data = []
training_labels = []
target_3selmer_curves = 5  # Stop after finding 5 curves with 3-Selmer rank >= 3
max_attempts = 100  # Maximum additional attempts
attempt = 54  # Continue from Attempt 54
current_fib_index = 44  # Start extending from index 44

# Existing high 3-Selmer rank curves
existing_high_selmer = [(2, 144, 3), (377, 987, 3), (34, 4181, 3)]