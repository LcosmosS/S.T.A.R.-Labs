    seen_pairs = seen_pairs or {}
    
    if force_failure and large_fibs:
        pair = random.sample(large_fibs, 2) if len(large_fibs) >= 2 else random.sample(valid_fibs, 2)
        if seen_pairs.get(tuple(pair), 0) < 1:
            return pair
        return random.sample(valid_fibs, 2)
    
    high_rank_pairs = [(2, 144), (233, 377), (144, 233), (89, 233), (34, 144), (21, 377), (5, 144), (3, 144), (13, 377), (34, 233), (89, 144), (377, 987), (5, 377), (13, 987)]
    high_rank_fibs = [2, 144, 233, 377, 89, 34, 21, 5, 3, 13, 987]
    
    if classifier is None or X_data is None or len(X_data) < 5:
        if random.random() < 0.999 and high_rank_pairs:
            available_pairs = [(a, b) for (a, b) in high_rank_pairs if seen_pairs.get((a, b), 0) < 1]
            if available_pairs:
                return random.choice(available_pairs)
        if len(high_rank_fibs) >= 2:
            pair = random.sample(high_rank_fibs, 2)
            if seen_pairs.get(tuple(pair), 0) < 1:
                return pair
        pair = random.sample(valid_fibs, 2)
        if seen_pairs.get(tuple(pair), 0) < 1:
            return pair
        return random.choice(high_rank_pairs)
    
    best_score = -float('inf')
    best_pair = None
    attempts = min(50, len(valid_fibs) * (len(valid_fibs) - 1) // 2)
    for _ in range(attempts):
        a, b = random.sample(valid_fibs, 2)
        if seen_pairs.get((a, b), 0) >= 1:
            continue
        delta = -16 * (4 * a**3 + 27 * b**2)
        log_delta = math.log(abs(delta)) if delta != 0 else 0
        log_cond = math.log(max(abs(a), abs(b), 1)) * 2
        tors_order = 1
        X = np.array([[a, b, log_delta, log_cond, tors_order]])
        score = classifier.predict_proba(X)[0, 1]
        if score > best_score:
            best_score = score
            best_pair = (a, b)
    return best_pair if best_pair else random.choice(high_rank_pairs)


def transform_curve(a, b, u):
    """
    Transform the elliptic curve y^2 = x^3 + ax + b by scaling x -> u^2 x, y -> u^3 y.
    Returns the new coefficients (a_new, b_new).
    """
