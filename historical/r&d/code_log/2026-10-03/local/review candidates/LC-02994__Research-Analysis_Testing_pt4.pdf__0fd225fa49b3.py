# Generate Fibonacci numbers
def generate_fibonacci(n):
    fib = [0, 1]
    for i in range(2, n + 1):
        fib.append(fib[i-1] + fib[i-2])
    return fib

# Initial Fibonacci numbers up to index 60
fib_numbers = generate_fibonacci(60)
print(f"Fibonacci numbers up to index 60: {fib_numbers}")

# Corrected training data for high 3-Selmer ranks
training_data = [
    [2, 144, 16.00810934168413, 15.314962161124182, 1],
    [377, 987, 22.07137262623868, 21.378225445678737, 1],
