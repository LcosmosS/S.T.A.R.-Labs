def generate_fibonacci(n):
fib = [0, 1]
for i in range(2, n + 1):
fib.append(fib[i-1] + fib[i-2])
return fib
fib_numbers = generate_fibonacci(77)
print(f"Fibonacci numbers up to index 77: {fib_numbers}")
