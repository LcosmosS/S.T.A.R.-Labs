    fib = [0, 1]
    if n < 2:
        return fib[:n+1]
    for i in range(2, n+1):
        fib.append(fib[i-1] + fib[i-2])
    return fib

def random_fibonacci_pair(n, classifier=None, fib_list=None, X_data=None, force_failure=False,
seen_pairs=None):
    """Select Fibonacci pair, heavily biased toward rank ≥ 3, controlling repetition."""
    if fib_list is None:
        fib_list = generate_fibonacci(n)
    valid_fibs = [f for f in fib_list if f != 0 and f <= 5000]
    large_fibs = [f for f in fib_list if f > 5000 and f <= 10000]
    if len(valid_fibs) < 2:
        return random.choice(fib_list), random.choice(fib_list)

    if force_failure and large_fibs:
        return random.sample(large_fibs, 2) if len(large_fibs) >= 2 else random.sample(valid_fibs, 2)

    # Expanded rank 3 candidates
    high_rank_pairs = [(2, 144), (8, 377), (13, 610), (5, 233), (3, 144), (2, 610), (3, 1597), (5, 144)]
    high_rank_fibs = [2, 144, 377, 610, 8, 13, 5, 233, 3, 1597]
    seen_pairs = seen_pairs or {}

    if classifier is None or X_data is None or len(X_data) < 10:
        if random.random() < 0.99 and high_rank_pairs:  # 99% bias for rank 3
            available_pairs = [(a, b) for (a, b) in high_rank_pairs if seen_pairs.get((a, b), 0) < (2 if (a, b) == (2,
