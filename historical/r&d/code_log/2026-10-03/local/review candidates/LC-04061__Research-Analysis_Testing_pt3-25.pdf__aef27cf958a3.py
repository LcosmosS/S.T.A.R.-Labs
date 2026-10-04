        return random.choice(fib_list), random.choice(fib_list)

    if force_failure and large_fibs:
        return random.sample(large_fibs, 2) if len(large_fibs) >= 2 else random.sample(valid_fibs, 2)

    high_rank_fibs = [2, 144, 5, 233, 377, 1, 34]  # Prioritize known rank 3 pair
    high_rank_pairs = [(2, 144), (5, 144), (34, 144)]  # Known rank 2–3 pairs
    if classifier is None or X_data is None or len(X_data) < 10:
        if random.random() < 0.8 and high_rank_pairs:  # Strong bias
            return random.choice(high_rank_pairs)
        if len(high_rank_fibs) >= 2:
            return random.sample(high_rank_fibs, 2)
        return random.sample(valid_fibs, 2)

    best_score = -float('inf')
    best_pair = None
    attempts = min(50, len(valid_fibs) * (len(valid_fibs) - 1) // 2)
    for _ in range(attempts):
        a, b = random.sample(valid_fibs, 2)
        delta = -16 * (4 * a**3 + 27 * b**2)
        log_delta = math.log(abs(delta)) if delta != 0 else 0
        log_cond = math.log(max(abs(a), abs(b), 1)) * 2
        tors_order = 1
        X = np.array([[a, b, log_delta, log_cond, tors_order]])
        score = classifier.predict_proba(X)[0, 1]
        if score > best_score:
            best_score = score
            best_pair = (a, b)
    return best_pair if best_pair else random.sample(valid_fibs, 2)

def analyze_curve(a, b, is_original=False, max_attempts=5, require_3selmer=False):
    """Analyze elliptic curve, estimating 3-Selmer without Magma."""
    curve_name = 'Original curve' if is_original else 'Fibonacci curve'
    print(f"\n{curve_name}: y² = x³ + {a}x + {b}")

    try:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
    except ValueError as e:
        print(f"Error creating curve: {e}")
        return False, None, None, None, None, None, None, False

    delta = E.discriminant()
    conductor = E.conductor()
    tors_order = E.torsion_subgroup().order()
    print(f"Discriminant: {delta}")
    print(f"Conductor: {conductor} = {factor(conductor)}")
    print(f"Torsion order: {tors_order} (cyclic nodes in 3-sphere interweb)")

    if conductor > 2e8 and not is_original:
