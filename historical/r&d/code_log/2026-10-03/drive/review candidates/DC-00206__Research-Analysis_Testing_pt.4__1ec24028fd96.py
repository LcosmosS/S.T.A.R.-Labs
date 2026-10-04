            for feat in rank3_features:
                synth_feat = [f + random.gauss(0, 0.4) for f in feat]
                X_data.append(synth_feat)
                y_data.append(1)
        classifier.fit(np.array(X_data), np.array(y_data))
        print(f"Classifier trained. Coefficients: {classifier.coef_}")
    
    a, b = random_fibonacci_pair(n, classifier, fib_numbers, X_data, force_failure, seen_pairs)
    if seen_pairs.get((a, b), 0) >= 1:
        print(f"Duplicate pair a={a}, b={b}, skipping")
        with open("failed_curves.txt", "a") as f:
            f.write(f"a={a},b={b},conductor=N/A,reason=duplicate\n")
        attempts += 1
        continue
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
            comoving_volume = (omega * reg * cosmo_scale**3) / (1e12 if rank == 3 else 3e12 if rank == 2 else 5e12 if rank == 1 else 1e13)
            scaled_reg = reg * SQRT_KAPPA * (20 if rank == 3 else 13 if rank == 2 else 10 if rank == 1 else 20)
            interweb_data.append((a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, features[2], features[3]))
            with open("interweb_nodes.txt", "a") as f:
                f.write(f"{a},{b},{rank},{leading_coeff},{omega},{reg},{tamagawa},{weak_bsd_holds},{features[2]},{features[3]}\n")
            with open("unique_curves.txt", "a") as f:
                conductor = E.conductor() if E else 'N/A'
                plot_file = f"curve_{a}_{b}.png" if E else 'N/A'
                f.write(f"{a},{b},{rank},{omega},{reg},{comoving_volume},{scaled_reg},{leading_coeff * 10 if leading_coeff else 0},{conductor},{plot_file}\n")
            successful_curves += 1
    attempts += 1


print(f"\nAnalyzing original curve")
success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E = analyze_curve(
    -1706, 6320, is_original=True, require_3selmer=require_3selmer
)
if features:
    X_data.append(features)
    y_data.append(success)
    if success and rank is not None:
        cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
        comoving_volume = (omega * reg * cosmo_scale**3) / 5e12  # Adjusted for original curve
        scaled_reg = reg * SQRT_KAPPA * (20 if rank == 3 else 13 if rank == 2 else 10 if rank == 1 else 20)
        interweb_data.append((-1706, 6320, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, features[2], features[3]))
        with open("interweb_nodes.txt", "a") as f:
            f.write(f"{-1706},{6320},{rank},{leading_coeff},{omega},{reg},{tamagawa},{weak_bsd_holds},{features[2]},{features[3]}\n")
        with open("unique_curves.txt", "a") as f:
            conductor = E.conductor() if E else 'N/A'
            plot_file = f"curve_{-1706}_{6320}.png" if E else 'N/A'
            f.write(f"{-1706},{6320},{rank},{omega},{reg},{comoving_volume},{scaled_reg},{leading_coeff * 10 if leading_coeff else 0},{conductor},{plot_file}\n")


if interweb_data:
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    node_counts = {}
    for node in interweb_data:
        key = (node[0], node[1], node[2])
        node_counts[key] = node_counts.get(key, 0) + 1
    filtered_data = []
    for node in interweb_data:
        key = (node[0], node[1], node[2])
        if node_counts[key] == 1:
            filtered_data.append(node)
            node_counts[key] -= 1
    
    ranks = [x[2] for x in filtered_data]
    log_deltas = [x[8] for x in filtered_data]
