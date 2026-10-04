    if n < 2:
        return fib[:n+1]
    for i in range(2, n+1):
        fib.append(fib[i-1] + fib[i-2])
    return fib


def random_fibonacci_pair(n, classifier=None, fib_list=None, X_data=None, force_failure=False, seen_pairs=None):
    """Selects Fibonacci pair, biased toward known high-rank candidates."""
    # (Simplified selection logic omitted for brevity in narrative context)
    # Target high_rank_pairs known to yield rank >= 3
    high_rank_pairs = [(2, 144), (5, 377), (34, 610), (3, 377), (5, 144), (34, 144), (2, 610), (3, 1597)]


    if random.random() < 0.98 and high_rank_pairs:
        # Bias towards known complex structures
        return random.choice(high_rank_pairs)


    # Fallback to random pair selection from filtered list (<= 5000)
