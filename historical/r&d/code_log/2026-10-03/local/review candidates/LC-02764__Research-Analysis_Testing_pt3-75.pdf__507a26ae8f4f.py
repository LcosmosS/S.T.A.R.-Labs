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