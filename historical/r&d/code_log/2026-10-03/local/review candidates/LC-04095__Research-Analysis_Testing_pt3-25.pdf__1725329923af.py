def random_fibonacci_pair(n, classifier=None, fib_list=None, X_data=None, force_failure=False,
seen_pairs=None):
    if fib_list is None:
        fib_list = generate_fibonacci(n)
