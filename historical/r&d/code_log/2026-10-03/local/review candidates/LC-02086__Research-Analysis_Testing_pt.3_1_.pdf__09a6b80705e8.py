    if len(valid_fibs) < 2:
        return random.choice(fib_list), random.choice(fib_list)

    if classifier is None or X_data is None:
        return random.sample(valid_fibs, 2)

    # Use classifier to score pairs
    best_score = -float('inf')
    best_pair = None
    attempts = min(50, len(valid_fibs) * (len(valid_fibs) - 1) // 2)
    for _ in range(attempts):
        a, b = random.sample(valid_fibs, 2)
        delta = -16 * (4 * a**3 + 27 * b**2)
        log_delta = math.log(abs(delta)) if delta != 0 else 0
        log_cond = math.log(max(abs(a), abs(b), 1)) * 2  # Placeholder
        tors_order = 1
        X = np.array([[a, b, log_delta, log_cond, tors_order]])
        score = classifier.predict_proba(X)[0, 1]  # Probability of success
        if score > best_score:
            best_score = score
            best_pair = (a, b)
    return best_pair if best_pair else random.sample(valid_fibs, 2)

def analyze_curve(a, b, is_original=False, max_attempts=5):
    """Analyze an elliptic curve, returning success status and features."""
    curve_name = 'Original curve' if is_original else 'Fibonacci curve'
    print(f"\n{curve_name}: y² = x³ + {a}x + {b}")

    try:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
    except ValueError as e:
        print(f"Error creating curve: {e}")
        return False, None

    delta = E.discriminant()
    conductor = E.conductor()
    tors_order = E.torsion_subgroup().order()
    print(f"Discriminant: {delta}")
    print(f"Conductor: {conductor} = {factor(conductor)}")
    print(f"Torsion order: {tors_order} (cyclic nodes in 3-sphere interweb)")

    rank_success = False
    selmer2_success = False
    selmer3_success = False
    rank = None
    selmer_rank = None
    selmer3_rank = None