def random_fibonacci_pair(n, classifier=None, fib_list=None, X_data=None):

    """Select a random Fibonacci pair, biased by classifier if provided."""

    if fib_list is None:

        fib_list = generate_fibonacci(n)

    valid_fibs = [f for f in fib_list if f != 0 and f <= 10000]  # Cap coefficients

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

        log_cond = math.log(max(abs(a), abs(b), 1)) * 2

        tors_order = 1

        X = np.array([[a, b, log_delta, log_cond, tors_order]])

        score = classifier.predict_proba(X)[0, 1]

        if score > best_score:

            best_score = score

            best_pair = (a, b)
    return best_pair if best_pair else random.sample(valid_fibs, 2)



def analyze_curve(a, b, is_original=False, max_attempts=5):

    """Analyze an elliptic curve, returning success status and features."""

    curve_name = 'Original curve' if is_original else 'Fibonacci curve'