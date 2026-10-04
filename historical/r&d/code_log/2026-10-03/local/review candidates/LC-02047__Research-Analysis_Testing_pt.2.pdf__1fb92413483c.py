# Define the Fibonacci function
def fibonacci(n):
    if n < 0:
        raise ValueError("Fibonacci sequence not defined for negative indices")
    if n == 0:
        return 0
    if n == 1:
        return 1
    fib = [0, 1]
    for i in range(2, n + 1):
        fib.append(fib[i-1] + fib[i-2])
    return fib[n]

# Define the pairs of indices for Fibonacci curves, plus the original curve
pairs = [(5, 7), (6, 8), (7, 9), (None, None)]  # (None, None) for the original curve

# Loop over each pair to construct and analyze the curve
for n1, n2 in pairs:
    if n1 is None and n2 is None:
        a = -1706
        b = 6320
        print(f"\nOriginal curve: y^2 = x^3 + {a}x + {b}")
    else:
        a = fibonacci(n1)
        b = fibonacci(n2)