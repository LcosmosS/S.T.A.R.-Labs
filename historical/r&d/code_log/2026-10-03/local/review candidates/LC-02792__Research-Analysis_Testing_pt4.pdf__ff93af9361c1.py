    seen_pairs[(a, b)] = seen_pairs.get((a, b), 0) + 1
    print(f"\nAttempt {attempts + 1}: Testing Fibonacci curve with a={a}, b={b}")
    success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E = analyze_curve(
        a, b, require_3selmer=require_3selmer
    )
    if features:
        X_data.append(features)
        y_data.append(success)
        if success and rank is not None:
            cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
            comoving_volume = (omega * reg * cosmo_scale**3) / (1e12 if rank == 3 else 3e12 if rank == 2
else 5e12 if rank == 1 else 1e13)
            scaled_reg = reg * SQRT_KAPPA * (20 if rank == 3 else 13 if rank == 2 else 10 if rank == 1 else
