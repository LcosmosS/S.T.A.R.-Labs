    return fib

def random_fibonacci_pair(n, classifier=None, fib_list=None, X_data=None, force_failure=False,
seen_pairs=None):
    if fib_list is None:
        fib_list = generate_fibonacci(n)
    valid_fibs = [f for f in fib_list if f != 0 and f <= 5000]
    large_fibs = [f for f in fib_list if f > 5000 and f <= 10000]
    seen_pairs = seen_pairs or {}

    if force_failure and large_fibs:
        pair = random.sample(large_fibs, 2) if len(large_fibs) >= 2 else random.sample(valid_fibs, 2)
        if seen_pairs.get(tuple(pair), 0) < 1:
            return pair
        return random.sample(valid_fibs, 2)

    high_rank_pairs = [(2, 144), (55, 377), (21, 233), (8, 233), (144, 377), (5, 144), (3, 144), (13, 377), (34,
