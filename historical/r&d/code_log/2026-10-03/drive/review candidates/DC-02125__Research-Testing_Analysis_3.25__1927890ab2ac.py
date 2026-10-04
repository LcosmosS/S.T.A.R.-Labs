                f.write(f"{a},{b},{rank},{leading_coeff},{omega},{reg},{tamagawa},{weak_bsd_holds},{features[2]},{features[3]}\n")
            successful_curves += 1
    attempts += 1


# Analyze original curve
print(f"\nAnalyzing original curve")
success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds = analyze_curve(
    -1706, 6320, is_original=True, require_3selmer=require_3selmer
)
if features:
    X_data.append(features)
    y_data.append(success)
    if success and rank is not None:
        interweb_data.append((-1706, 6320, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, features[2], features[3]))
        with open("interweb_nodes.txt", "a") as f:
            f.write(f"{-1706},{6320},{rank},{leading_coeff},{omega},{reg},{tamagawa},{weak_bsd_holds},{features[2]},{features[3]}\n")


# Plot interweb with distance annotations
if interweb_data:
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    ranks = [x[2] for x in interweb_data]
    log_deltas = [x[8] for x in interweb_data]
