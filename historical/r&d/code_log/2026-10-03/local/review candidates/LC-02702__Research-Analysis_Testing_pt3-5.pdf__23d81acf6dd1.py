            successful_curves += 1
    attempts += 1

# Analyze original curve
print(f"\nAnalyzing original curve")
success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E = analyze_curve(
    -1706, 6320, is_original=True, require_3selmer=require_3selmer
)
if features:
    X_data.append(features)
    y_data.append(success)
    if success and rank is not None:
        cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
        comoving_volume = (omega * reg * cosmo_scale**3) / 1e14
        scaled_reg = reg * SQRT_KAPPA * (20 if rank == 3 else 10 if rank == 2 else 20 if rank == 1 else 20)
        interweb_data.append((-1706, 6320, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
