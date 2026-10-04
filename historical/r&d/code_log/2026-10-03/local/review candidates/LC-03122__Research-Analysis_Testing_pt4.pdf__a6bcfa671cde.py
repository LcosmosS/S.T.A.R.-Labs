    gc.collect()

# Twist the curve (a=34, b=-34) with d=5
print("\nTwisting curve (a=34, b=-34) to find a higher rank...")
d = 5
a_new = 34 * d
b_new = -34 * (d**3)
E_twist = EllipticCurve(QQ, [0, 0, 0, a_new, b_new])
print(f"Twisted curve: y² = x³ + {a_new}x + {b_new}")
try:
    result = analyze_curve(a_new, b_new, conductor_limit=1e14)
    if len(result) == 10:
        success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
E, selmer3_rank = result
        if success:
            results.append(("Twist2", (a_new, b_new, rank, normalized_leading_coeff, omega, reg,
