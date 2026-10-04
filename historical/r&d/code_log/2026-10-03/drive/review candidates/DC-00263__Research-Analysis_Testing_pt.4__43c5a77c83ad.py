training_labels = [3, 3, 3, 3, 3]
print(f"Corrected training data: {training_data}")
print(f"Corrected labels: {training_labels}")


# Function to compute discriminant
def compute_discriminant(a, b):
    return -16 * (4 * a**3 + 27 * b**2)


# Target 7 curves with 3-Selmer rank >= 3
target_3selmer_curves = 7
max_attempts = 100
attempt = 71
current_fib_index = 62
phi_powers = [0, 1, 2]


# Continuous testing loop
while len(training_data) < target_3selmer_curves and attempt <= 70 + max_attempts:
    # Extend Fibonacci sequence if needed
    if current_fib_index >= len(fib_numbers):
        fib_numbers.append(fib_numbers[-1] + fib_numbers[-2])
        print(f"Extended Fibonacci numbers to index {current_fib_index}: {fib_numbers[-1]}")
    current_fib_index += 1
    
    # Select a and b indices
    a_idx = (attempt - 71) % 20
    b_idx = (attempt - 71) % len(fib_numbers)
    fib_a = fib_numbers[a_idx]
    fib_b = fib_numbers[b_idx]
    
    # Alternate golden ratio scaling and introduce negative coefficients
    phi_idx = (attempt - 71) % len(phi_powers)
    if (attempt - 71) % 2 == 0:
        sign = -1 if (attempt - 71) % 4 == 0 else 1
        a = sign * int(round(fib_a * (PHI ** phi_powers[phi_idx])))
        b = fib_b
        print(f"\nAttempt {attempt}: Testing Fibonacci curve with a={a} (φ^{phi_powers[phi_idx]} * {fib_a} * {sign}), b={b} (raw)")
    else:
        a = fib_a
        sign = -1 if (attempt - 71) % 4 == 1 else 1
        b = sign * int(round(fib_b * (PHI ** phi_powers[phi_idx])))
        print(f"\nAttempt {attempt}: Testing Fibonacci curve with a={a} (raw), b={b} (φ^{phi_powers[phi_idx]} * {fib_b} * {sign})")
    
    # Check discriminant to avoid singular curves
    delta = compute_discriminant(a, b)
    if delta == 0:
        print(f"Discriminant is 0 for a={a}, b={b}, skipping curve")
        attempt += 1
        continue
    
    result = analyze_curve(a, b, require_3selmer=False, conductor_limit=1e14, descent_limit=20)
    
    # Handle the return value safely
    if len(result) == 10:
        success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank = result
    else:
        print("Curve analysis failed, skipping...")
        attempt += 1
        continue
    
    if success and rank is not None:
        # Add to interweb_data
        if omega is not None and reg is not None:
            interweb_data.append((a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, features[2], features[3]))
            with open("interweb_nodes.txt", "a") as f:
                f.write(f"{a},{b},{rank},{normalized_leading_coeff},{omega},{reg},{tamagawa},{weak_bsd_holds},{features[2]},{features[3]}\n")
            with open("unique_curves.txt", "a") as f:
                conductor = E.conductor() if E else 'N/A'
                plot_file = f"curve_{a}_{b}.png" if E else 'N/A'
                cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
                comoving_volume = (omega * reg * cosmo_scale**3) / (2.5e11 if rank == 3 else 3e12 if rank == 2 else 5e14 if rank == 1 else 1e13)
                scaled_reg = reg * SQRT_KAPPA * (20 if rank == 3 else 13 if rank == 2 else 60 if rank == 1 else 20)
                f.write(f"{a},{b},{rank},{omega},{reg},{comoving_volume},{scaled_reg},{normalized_leading_coeff * 10},{conductor},{plot_file}\n")
        
        # Check for high 3-Selmer rank
        if selmer3_rank is not None and selmer3_rank >= 3:
            if features not in training_data:
                training_data.append(features)
                training_labels.append(selmer3_rank)
                print(f"Found high 3-Selmer rank curve: a={a}, b={b}, 3-Selmer rank={selmer3_rank}")
                print(f"Current training data: {training_data}")
                print(f"Current labels: {training_labels}")
    
    # Regenerate interweb plot
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
            if node_counts[key] > 0:
                filtered_data.append(node)
                node_counts[key] -= 1
        
        ranks = [x[2] for x in filtered_data]
        log_deltas = [x[8] for x in filtered_data]
