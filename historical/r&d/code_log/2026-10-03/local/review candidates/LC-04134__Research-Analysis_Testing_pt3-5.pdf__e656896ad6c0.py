        fib.append(fib[i-1] + fib[i-2])
    return fib

def random_fibonacci_pair(n, classifier=None, fib_list=None, X_data=None, force_failure=False,
seen_pairs=None):
    """Select Fibonacci pair, heavily biased toward rank ≥ 3, no repetition."""
    if fib_list is None:
        fib_list = generate_fibonacci(n)
