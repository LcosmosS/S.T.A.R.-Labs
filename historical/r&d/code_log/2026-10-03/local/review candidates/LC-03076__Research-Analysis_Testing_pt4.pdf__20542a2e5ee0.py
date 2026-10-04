    delta = compute_discriminant(a, b)
    if delta == 0:
        print(f"Discriminant is 0 for a={a}, b={b}, skipping curve")
        attempt += 1
        continue

    result = analyze_curve(a, b, conductor_limit=1e14)
    if len(result) == 10:
        success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
E, selmer3_rank = result
        if success:
            results.append((attempt, (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa,
