# Generate Fibonacci numbers
def generate_fibonacci(n):
    fib = [0, 1]
    for i in range(2, n + 1):
        fib.append(fib[i-1] + fib[i-2])
    return fib

# Initial Fibonacci numbers up to index 61
fib_numbers = generate_fibonacci(61)
print(f"Fibonacci numbers up to index 61: {fib_numbers}")

# Corrected training data for high 3-Selmer ranks
training_data = [
    [2, 144, 16.0081093416841, 15.31496216112418, 1],
    [377, 987, 22.0713726262387, 21.37822544567874, 1],
