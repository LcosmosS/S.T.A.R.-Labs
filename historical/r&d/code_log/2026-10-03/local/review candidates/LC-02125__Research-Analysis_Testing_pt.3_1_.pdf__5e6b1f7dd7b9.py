            interweb_data.append((a, b, rank, leading_coeff, omega, reg, features[2], features[3]))


    if success and rank is not None:  # Accept all ranks


        successful_curves += 1


    attempts += 1





# Analyze original curve


print(f"\nAnalyzing original curve")


success, features, rank, leading_coeff, omega, reg = analyze_curve(-1706, 6320, is_original=True,
require_3selmer=require_3selmer)


if features:


    X_data.append(features)


    y_data.append(success)


    if success and rank is not None:


        interweb_data.append((-1706, 6320, rank, leading_coeff, omega, reg, features[2], features[3]))





# Save interweb data


with open("interweb_nodes.txt", "w") as f:


    f.write("a,b,rank,leading_coeff,omega,regulator,log_delta,log_cond\n")


    for a, b, rank, lc, omega, reg, ld, lcnd in interweb_data:


        f.write(f"{a},{b},{rank},{lc},{omega},{reg},{ld},{lcnd}\n")