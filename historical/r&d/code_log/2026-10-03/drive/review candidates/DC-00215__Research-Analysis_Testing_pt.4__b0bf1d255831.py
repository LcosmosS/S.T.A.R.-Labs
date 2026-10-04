interweb_data = [
    (13, 377, 0, 1.5248784246208363956283412258 / 10, 1.5248784246208363956283412258, 1.0, 1, True, math.log(61540336), math.log(61540336)),
    (2, 144, 3, 35.620854002542971603630883958 / 10, 1.8236602565125279190648710531, 9.76630758808727, 2, True, math.log(8958464), math.log(4479232)),
    (144, 233, 1, 14.397681380538820045587978770 / 10, 1.1093071817654113436605273746, 2.16316418289501, 6, True, math.log(214555824), math.log(17879652)),
    (34, 144, 2, 12.623558290853645758994107725 / 10, 1.5874476029557543327015819683, 3.97605510485800, 2, True, math.log(11473408), math.log(5736704)),
    (13, 987, 1, 13.039158348750303747140334275 / 10, 1.3151800172294174231558959060, 4.95717627166311, 2, True, math.log(420981616), math.log(210490808)),
    (3, 89, 1, 6.4324388344582834500532471427 / 10, 1.9600188761307938499775937804, 1.64091247099526, 2, True, math.log(3423600), math.log(171180)),
    (233, 377, 1, 42.519873284318607465001911780 / 10, 0.97788673099329385551811276549, 43.4813889346150, 1, True, math.log(870957296), math.log(870957296)),
    (377, 987, 3, 90.806664941709888414870399502 / 10, 0.87208122227906561171302115761, 52.0631924079268, 2, True, math.log(3850129520), math.log(1925064760)),
    (21, 377, 2, 48.908235212032508551081877140 / 10, 1.4996021175316803131515116071, 32.6141412046914, 1, True, math.log(61992432), math.log(61992432)),
    (89, 144, 1, 2.9437200606692904381404309311 / 10, 1.2586015062787318056673340499, 2.33888172386898, 1, True, math.log(54075968), math.log(54075968)),
]


classifier = None
max_successful_curves = 30
max_total_attempts = 35
n = 25
require_3selmer = False
successful_curves = 10  # From the first 10 attempts
attempts = 10  # Start from attempt 11
fib_numbers = generate_fibonacci(n)
print(f"Fibonacci numbers up to index {n}: {fib_numbers}")


# Reinitialize output files to append new results
with open("interweb_nodes.txt", "w") as f:
    f.write("a,b,rank,normalized_leading_coeff,omega,regulator,tamagawa,weak_bsd_holds,log_delta,log_cond\n")
with open("failed_curves.txt", "w") as f:
    f.write("a,b,conductor,reason\n")
with open("rank3_curves.txt", "w") as f:
    f.write("a,b,rank,selmer3,volume\n")
with open("unique_curves.txt", "w") as f:
    f.write("a,b,rank,omega,reg,volume,scaled_reg,leading_coeff,conductor,plot_file\n")


# Rewrite the first 10 attempts to the output files
for data in interweb_data:
    a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, log_delta, log_cond = data
    cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
    comoving_volume = (omega * reg * cosmo_scale**3) / (3e11 if rank == 3 else 3e12 if rank == 2 else 5e12 if rank == 1 else 1e13)
    scaled_reg = reg * SQRT_KAPPA * (20 if rank == 3 else 13 if rank == 2 else 60 if rank == 1 else 20)
    with open("interweb_nodes.txt", "a") as f:
        f.write(f"{a},{b},{rank},{leading_coeff},{omega},{reg},{tamagawa},{weak_bsd_holds},{log_delta},{log_cond}\n")
    with open("unique_curves.txt", "a") as f:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        conductor = E.conductor()
        plot_file = f"curve_{a}_{b}.png"
        f.write(f"{a},{b},{rank},{omega},{reg},{comoving_volume},{scaled_reg},{leading_coeff * 10},{conductor},{plot_file}\n")
    if rank >= 3:
        with open("rank3_curves.txt", "a") as f:
            f.write(f"a={a},b={b},rank={rank},selmer3={rank},volume={comoving_volume}\n")


# Continue the loop from attempt 11
while successful_curves < max_successful_curves and attempts < max_total_attempts:
    force_failure = (attempts % 5 == 0 and attempts > 0 and len(set(y_data)) < 2)
    if attempts % 10 == 0 and len(X_data) >= 5:
        print("\nTraining logistic regression classifier...")
        # Check if we have at least two classes
        if len(set(y_data)) < 2:
            print("Only one class in y_data, introducing synthetic failures...")
            # Add synthetic failures by perturbing existing features
            for i in range(min(5, len(X_data))):  # Add up to 5 synthetic failures
                synth_feat = [f + random.gauss(0, 0.5) for f in X_data[i]]
                X_data.append(synth_feat)
                y_data.append(0)
        classifier = LogisticRegression(max_iter=1000, class_weight={1: 50, 0: 1})
        # Augment with synthetic rank 3 features
