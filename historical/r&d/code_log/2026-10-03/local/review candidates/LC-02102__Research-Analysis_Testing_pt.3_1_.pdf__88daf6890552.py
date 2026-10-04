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


    """Analyze an elliptic curve, returning success status and features."""


    curve_name = 'Original curve' if is_original else 'Fibonacci curve'


    print(f"\n{curve_name}: y² = x³ + {a}x + {b}")