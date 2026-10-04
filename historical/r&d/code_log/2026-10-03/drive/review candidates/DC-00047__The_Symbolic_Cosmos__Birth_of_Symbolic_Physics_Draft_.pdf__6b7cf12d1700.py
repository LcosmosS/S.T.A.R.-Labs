fib = [0, 1]
if n < 2:
return fib[:n+1]
for i in range(2, n+1):
fib.append(fib[i-1] + fib[i-2])
return fib
def random_fibonacci_pair(n, classifier=None, fib_list=None, X_data=None,
force_failure=False):
"""Select a random Fibonacci pair, biased toward rank ≥ 3 or successful curves."""
if fib_list is None:
fib_list = generate_fibonacci(n)
