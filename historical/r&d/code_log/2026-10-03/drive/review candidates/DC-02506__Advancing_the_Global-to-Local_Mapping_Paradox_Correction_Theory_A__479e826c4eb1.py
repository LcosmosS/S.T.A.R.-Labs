    for a, b in previous_curves:
        result = analyze_curve(a, b, conductor_limit=conductor_limit)
        if len(result) == 10:
            success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank = result
            if success:
                curves_data.append((None, (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank, features)))
        gc.collect()
    
    # Generate new curves
    for _ in range(max_attempts):
        a, b = random_fibonacci_pair(fib_numbers, lucas_numbers, high_rank_pairs)
        result = analyze_curve(a, b, conductor_limit=conductor_limit)
        if len(result) == 10:
            success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank = result
            if success:
                curves_data.append((None, (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank, features)))
                if rank >= 3:
                    training_data.append(features)
                    training_labels.append(rank)
                    print(f"Added new rank {rank} curve to training data: {features}")
        gc.collect()
    
    # Quadratic twists for high-rank candidates
    twist_primes = [2, 3, 5, 7]
    for a, b in high_rank_pairs:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        for d in twist_primes:
            E_twist = quadratic_twist(E, d)
            a_new = E_twist.a4()
            b_new = E_twist.a6()
            print(f"\nTwisting curve (a={a}, b={b}) with d={d}")
            result = analyze_curve(a_new, b_new, conductor_limit=conductor_limit)
            if len(result) == 10:
                success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E_twist, selmer3_rank = result
                if success:
                    curves_data.append((f"Twist_d{d}", (a_new, b_new, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E_twist, selmer3_rank, features)))
                    if rank >= 3:
                        training_data.append(features)
                        training_labels.append(rank)
                        print(f"Added twisted rank {rank} curve to training data: {features}")
            gc.collect()
    
    # Train classifier
    try:
