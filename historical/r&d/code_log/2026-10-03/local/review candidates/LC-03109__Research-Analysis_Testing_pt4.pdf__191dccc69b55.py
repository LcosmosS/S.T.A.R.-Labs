# Twist the curve (a=-1597, b=987) with d=3
print("\nTwisting curve (a=-1597, b=987) to find a higher rank...")
d = 3
a_new = -1597 * d
b_new = 987 * (d**3)
E_twist = EllipticCurve(QQ, [0, 0, 0, a_new, b_new])
print(f"Twisted curve: y² = x³ + {a_new}x + {b_new}")
try:
    result = analyze_curve(a_new, b_new, conductor_limit=1e14)
    if len(result) == 10:
        success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
E, selmer3_rank = result
        if success:
            results.append(("Twist", (a_new, b_new, rank, normalized_leading_coeff, omega, reg,
