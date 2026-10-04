# Cosmological constants
KAPPA = 1000
SQRT_KAPPA = math.sqrt(KAPPA)  # ≈ 31.6
VIRGO_DISTANCE = 54e6
VIRGO_COMOVING_VOLUME = 1e9
DENSITY_HEIGHT_TARGET = 6320

def generate_fibonacci(n):
    """Generate Fibonacci numbers up to index n."""
    fib = [0, 1]
    if n < 2:
        return fib[:n+1]
    for i in range(2, n+1):
        fib.append(fib[i-1] + fib[i-2])
    return fib

def random_fibonacci_pair(n, classifier=None, fib_list=None, X_data=None, force_failure=False,
seen_pairs=None):
    """Select Fibonacci pair, biased toward rank ≥ 3, avoiding over-repetition."""
    if fib_list is None:
        fib_list = generate_fibonacci(n)
    valid_fibs = [f for f in fib_list if f != 0 and f <= 5000]
    large_fibs = [f for f in fib_list if f > 5000 and f <= 10000]
    if len(valid_fibs) < 2:
        return random.choice(fib_list), random.choice(fib_list)

    if force_failure and large_fibs:
        return random.sample(large_fibs, 2) if len(large_fibs) >= 2 else random.sample(valid_fibs, 2)

    high_rank_pairs = [(2, 144), (2, 610), (5, 377), (5, 144), (34, 144), (2, 233)]  # New rank 3 candidates
    high_rank_fibs = [2, 144, 610, 377, 5, 34, 233]
    seen_pairs = seen_pairs or {}

    if classifier is None or X_data is None or len(X_data) < 10:
        if random.random() < 0.9 and high_rank_pairs:  # Stronger bias
            available_pairs = [(a, b) for (a, b) in high_rank_pairs if seen_pairs.get((a, b), 0) < 2]
            if available_pairs:
                return random.choice(available_pairs)
        if len(high_rank_fibs) >= 2:
            pair = random.sample(high_rank_fibs, 2)
            if seen_pairs.get(tuple(pair), 0) < 2:
                return pair
        pair = random.sample(valid_fibs, 2)
        if seen_pairs.get(tuple(pair), 0) < 2:
            return pair
        return random.choice(high_rank_pairs)  # Fallback

    best_score = -float('inf')
    best_pair = None