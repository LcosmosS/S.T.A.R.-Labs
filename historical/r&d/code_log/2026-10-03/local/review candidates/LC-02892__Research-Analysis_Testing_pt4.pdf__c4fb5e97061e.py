    if rank >= 3:
        with open("rank3_curves.txt", "a") as f:
            f.write(f"a={a},b={b},rank={rank},selmer3={rank},volume={comoving_volume}\n")

# Retry attempt 18 with new rank computation strategy
print(f"\nRetrying Attempt 18: Testing Fibonacci curve with a=2584, b=144")
success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E = analyze_curve(
    2584, 144, require_3selmer=require_3selmer, conductor_limit=1e11
)
if features:
    X_data.append(features)
    y_data.append(success)
    if success and rank is not None:
        cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
        comoving_volume = (omega * reg * cosmo_scale**3) / (3e11 if rank == 3 else 3e12 if rank == 2 else
5e12 if rank == 1 else 1e13)
        scaled_reg = reg * SQRT_KAPPA * (20 if rank == 3 else 13 if rank == 2 else 60 if rank == 1 else 20)
        interweb_data.append((2584, 144, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
