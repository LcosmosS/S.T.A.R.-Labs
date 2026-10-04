    return fib


def random_fibonacci_pair(n, classifier=None, fib_list=None, X_data=None, high_rank_pairs=[]):
    """Select a Fibonacci pair, biased toward known high-rank candidates."""
    if fib_list is None: fib_list = generate_fibonacci(n)
    valid_fibs = [f for f in fib_list if f != 0]
    
    # 99.8% bias to test known high-rank pairs
    if random.random() < 0.998 and high_rank_pairs:
        return random.choice(high_rank_pairs)


    # Use classifier to score and select pairs
    if classifier and X_data:
        best_score = -float('inf')
        best_pair = None
        for _ in range(50): # Test 50 random pairs
            a, b = random.sample(valid_fibs, 2)
            delta = -16 * (4 * a**3 + 27 * b**2)
            log_delta = math.log(abs(delta)) if delta != 0 else 0
            log_cond = math.log(max(abs(a), abs(b), 1)) * 2 # Placeholder
            tors_order = 1
            X = np.array([[a, b, log_delta, log_cond, tors_order]])
            score = classifier.predict_proba(X)[0, 1]
            if score > best_score:
                best_score = score
                best_pair = (a, b)
        return best_pair if best_pair else random.sample(valid_fibs, 2)
    
    return random.sample(valid_fibs, 2)


def analyze_curve(a, b, is_original=False):
    """
    Analyzes an elliptic curve, computes its invariants, and maps them
