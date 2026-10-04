# Generate Fibonacci numbers
def generate_fibonacci(n):
    fib = [0, 1]
    for i in range(2, n + 1):
        fib.append(fib[i-1] + fib[i-2])
    return fib

# Initial Fibonacci numbers up to index 25
fib_numbers = generate_fibonacci(25)
print(f"Initial Fibonacci numbers: {fib_numbers}")

# Training data for high 3-Selmer ranks
