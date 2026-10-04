    # Check discriminant to avoid singular curves
    delta = compute_discriminant(a, b)
    if delta == 0:
        print(f"Discriminant is 0 for a={a}, b={b}, skipping curve")
        attempt += 1
        continue

    result = analyze_curve(a, b, require_3selmer=False, conductor_limit=1e14, descent_limit=20)

    # Handle the return value safely
    if len(result) == 10:
        success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E,
selmer3_rank = result
    else:
        print("Curve analysis failed, skipping...")
        attempt += 1
        continue

    if success and rank is not None:
        # Add to interweb_data
        if omega is not None and reg is not None:
            interweb_data.append((a, b, rank, normalized_leading_coeff, omega, reg, tamagawa,
