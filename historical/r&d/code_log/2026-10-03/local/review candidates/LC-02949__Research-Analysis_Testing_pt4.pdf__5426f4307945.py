def analyze_curve(a, b, is_original=False, max_attempts=5, require_3selmer=False,
conductor_limit=1e11, descent_limit=20):
    curve_name = 'Original curve' if is_original else 'Fibonacci curve'
    print(f"\n{curve_name}: y² = x³ + {a}x + {b}")

    try:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
    except ValueError as e:
        print(f"Error creating curve: {e}")