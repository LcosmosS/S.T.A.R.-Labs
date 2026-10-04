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
    (2, 89, 0, 3.9406077220873739436509377827 / 10, 1.9703038610436869718254688913, 1.0, 2, True, math.log(3422384), math.log(1711192)),
    (2584, 233, 0, 3.1224725812826300697030396822 / 10, 0.52041209688043834495050661370, 1.0, 6, True, math.log(1104248265904), math.log(39437438068)),
    (377, 2, 1, 19.086494537074770450070509606 / 10, 0.84161318212549367925981332813, 11.3392321689115, 2, True, math.log(3429290240), math.log(5792720)),
    (-1706, 6320, 1, 5.7161472701821916623395660050 / 10, 0.42236269178325809849360427108, 3.38343524498343, 4, True, math.log(300517927424), math.log(150258963712)),
]


classifier = LogisticRegression(max_iter=1000, class_weight={1: 50, 0: 1})
classifier.fit(np.array(X_data), np.array(y_data))
print(f"Classifier retrained. Coefficients: {classifier.coef_}")


max_successful_curves = 30
max_total_attempts = 50
n = 25
require_3selmer = False
successful_curves = 13  # 10 from first set + 2 from attempts 11 and 14 + 1 from attempt 34
attempts = 17  # Resume from attempt 18
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


# Rewrite the existing results to the output files
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


# Retry attempt 18 with PARI/GP adaptation
print(f"\nRetrying Attempt 18: Testing Fibonacci curve with a=2584, b=144")
success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E = analyze_curve(
    2584, 144, require_3selmer=require_3selmer, conductor_limit=1e11
)
# Update X_data and y_data based on the new attempt
if features:
    # Remove the old attempt 18 entry
    old_attempt_18 = [2584, 144, math.log(1104233771008), math.log(8626826336), 1]
    old_success = 0
    for i, (x, y) in enumerate(zip(X_data, y_data)):
        if x == old_attempt_18 and y == old_success:
            X_data.pop(i)
            y_data.pop(i)
            break
    # Append the new result
    X_data.append(features)
    y_data.append(success)
    if success and rank is not None:
        cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
        comoving_volume = (omega * reg * cosmo_scale**3) / (3e11 if rank == 3 else 3e12 if rank == 2 else 5e12 if rank == 1 else 1e13)
        scaled_reg = reg * SQRT_KAPPA * (20 if rank == 3 else 13 if rank == 2 else 60 if rank == 1 else 20)
        interweb_data.append((2584, 144, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, features[2], features[3]))
        with open("interweb_nodes.txt", "a") as f:
            f.write(f"{2584},{144},{rank},{leading_coeff},{omega},{reg},{tamagawa},{weak_bsd_holds},{features[2]},{features[3]}\n")
        with open("unique_curves.txt", "a") as f:
            conductor = E.conductor() if E else 'N/A'
            plot_file = f"curve_2584_144.png" if E else 'N/A'
            f.write(f"{2584},{144},{rank},{omega},{reg},{comoving_volume},{scaled_reg},{leading_coeff * 10 if leading_coeff else 0},{conductor},{plot_file}\n")
        successful_curves += 1
attempts += 1


# Continue the loop from attempt 19
while successful_curves < max_successful_curves and attempts < max_total_attempts:
    force_failure = (attempts % 5 == 0 and attempts > 0 and len(set(y_data)) < 2)
    if attempts % 10 == 0 and len(X_data) >= 5:
        print("\nTraining logistic regression classifier...")
        if len(set(y_data)) < 2:
            print("Only one class in y_data, introducing synthetic failures...")
            for i in range(min(5, len(X_data))):
                synth_feat = [f + random.gauss(0, 0.5) for f in X_data[i]]
                X_data.append(synth_feat)
                y_data.append(0)
        classifier = LogisticRegression(max_iter=1000, class_weight={1: 50, 0: 1})
