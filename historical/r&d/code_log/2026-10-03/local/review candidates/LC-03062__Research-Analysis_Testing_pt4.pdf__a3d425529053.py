    delta = compute_discriminant(a, b)
    if delta == 0:
        print(f"Discriminant is 0 for a={a}, b={b}, skipping curve")
        attempt += 1
        continue

    result = analyze_curve(a, b, conductor_limit=1e14)
    if len(result) == 10:
        success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
E, selmer3_rank = result
        if success and selmer3_rank is not None and selmer3_rank >= 3:
            if features not in training_data:
                training_data.append(features)
                training_labels.append(selmer3_rank)
                print(f"Found high 3-Selmer rank curve: a={a}, b={b}, 3-Selmer rank={selmer3_rank}")
    else:
        print("Curve analysis failed, skipping...")

    # Memory management
    gc.collect()
    attempt += 1

# Heegner point analysis
print("\n--- Heegner Point Analysis ---")
# Curve (a=34, b=-34)
print("\nAnalyzing curve (a=34, b=-34) for Heegner points...")
E1 = EllipticCurve(QQ, [0, 0, 0, 34, -34])
print(f"Curve: {E1}")
N1 = E1.conductor()
print(f"Conductor: {N1}")
try:
    heegner = E1.heegner_point(-7)