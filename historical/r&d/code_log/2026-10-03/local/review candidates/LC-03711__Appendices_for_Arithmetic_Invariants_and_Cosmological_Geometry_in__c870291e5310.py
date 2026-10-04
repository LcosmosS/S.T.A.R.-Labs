    if compute_discriminant(a, b) == 0:
        print("Singular curve (discriminant is 0), skipping...")
        attempt += 1
        continue

    result = analyze_curve(a, b, conductor_limit=1e14)

    if len(result) == 10:
        success, features, rank, _, _, _, _, _, _, selmer3_rank = result
        if success and selmer3_rank is not None and selmer3_rank >= 3:
