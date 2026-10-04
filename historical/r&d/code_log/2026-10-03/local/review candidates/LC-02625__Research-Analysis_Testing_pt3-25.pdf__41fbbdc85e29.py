def random_fibonacci_pair(n, classifier=None, fib_list=None, X_data=None, force_failure=False,
seen_pairs=None):
    if fib_list is None:
        fib_list = generate_fibonacci(n)
    valid_fibs = [f for f in fib_list if f != 0 and f <= 5000]
    large_fibs = [f for f in fib_list if f > 5000 and f <= 10000]
    if len(valid_fibs) < 2:
        return random.choice(fib_list), random.choice(fib_list)

    if force_failure and large_fibs:
        return random.sample(large_fibs, 2) if len(large_fibs) >= 2 else random.sample(valid_fibs, 2)

    high_rank_pairs = [(2, 144), (5, 377), (34, 610), (3, 377), (5, 144), (34, 144), (2, 610)]  # New
