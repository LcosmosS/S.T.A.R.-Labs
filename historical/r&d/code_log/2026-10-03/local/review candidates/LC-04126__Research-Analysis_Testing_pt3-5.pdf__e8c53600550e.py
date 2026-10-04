    if force_failure and large_fibs:
        return random.sample(large_fibs, 2) if len(large_fibs) >= 2 else random.sample(valid_fibs, 2)

    # New rank 3 candidates
    high_rank_pairs = [(2, 144), (5, 377), (34, 610), (3, 233), (8, 144), (13, 377), (5, 610)]
    high_rank_fibs = [2, 144, 377, 610, 5, 34, 233, 8, 13]
    seen_pairs = seen_pairs or {}

    if classifier is None or X_data is None or len(X_data) < 10:
        if random.random() < 0.99 and high_rank_pairs:  # 99% bias
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
    return best_pair if best_pair and seen_pairs.get(best_pair, 0) < 1 else random.choice(high_rank_pairs)

def analyze_curve(a, b, is_original=False, max_attempts=5, require_3selmer=False):
    """Analyze elliptic curve, return curve object, enhanced polynomial plot."""
    curve_name = 'Original curve' if is_original else 'Fibonacci curve'
    print(f"\n{curve_name}: y² = x³ + {a}x + {b}")

    E = None
    try:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
    except ValueError as e:
