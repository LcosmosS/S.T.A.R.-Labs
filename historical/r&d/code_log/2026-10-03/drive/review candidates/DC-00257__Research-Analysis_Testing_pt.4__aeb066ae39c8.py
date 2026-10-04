training_labels = [3, 3, 3, 3, 3]
print(f"Corrected training data: {training_data}")
print(f"Corrected labels: {training_labels}")


# We already have 5 curves, but let's continue to find more for a better dataset
target_3selmer_curves = 7  # Aim for 7 curves to improve the classifier
max_attempts = 100  # Maximum additional attempts
attempt = 71  # Continue from Attempt 71
current_fib_index = 61  # Start extending from index 61


# Continuous testing loop with refined golden ratio scaling
phi_powers = [0, 1, 2]  # Test scaling by φ^0, φ^1, φ^2
while len(training_data) < target_3selmer_curves and attempt <= 70 + max_attempts:
    # Extend Fibonacci sequence if needed
    if current_fib_index >= len(fib_numbers):
        fib_numbers.append(fib_numbers[-1] + fib_numbers[-2])
        print(f"Extended Fibonacci numbers to index {current_fib_index}: {fib_numbers[-1]}")
    current_fib_index += 1
    
    # Select a and b indices, pairing smaller and larger Fibonacci numbers
    a_idx = (attempt - 71) % 20  # Use smaller Fibonacci numbers (indices 0 to 19)
    b_idx = (attempt - 71) % len(fib_numbers)  # Use larger Fibonacci numbers
    fib_a = fib_numbers[a_idx]
    fib_b = fib_numbers[b_idx]
    
    # Alternate golden ratio scaling: scale a, keep b raw, or vice versa
    phi_idx = (attempt - 71) % len(phi_powers)
    if (attempt - 71) % 2 == 0:
        # Scale a, keep b raw
        a = int(round(fib_a * (PHI ** phi_powers[phi_idx])))
        b = fib_b
        print(f"\nAttempt {attempt}: Testing Fibonacci curve with a={a} (φ^{phi_powers[phi_idx]} * {fib_a}), b={b} (raw)")
    else:
        # Keep a raw, scale b
        a = fib_a
        b = int(round(fib_b * (PHI ** phi_powers[phi_idx])))
        print(f"\nAttempt {attempt}: Testing Fibonacci curve with a={a} (raw), b={b} (φ^{phi_powers[phi_idx]} * {fib_b})")
    
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
                comoving_volume = (omega * reg * cosmo_scale**3) / (2.5e11 if rank == 3 else 3e12 if rank == 2 else 5e12 if rank == 1 else 1e13)
                scaled_reg = reg * SQRT_KAPPA * (20 if rank == 3 else 13 if rank == 2 else 60 if rank == 1 else 20)
                f.write(f"{a},{b},{rank},{omega},{reg},{comoving_volume},{scaled_reg},{normalized_leading_coeff * 10},{conductor},{plot_file}\n")
        
        # Check for high 3-Selmer rank
        if selmer3_rank is not None and selmer3_rank >= 3:
            # Avoid duplicates in training data
            if features not in training_data:
                training_data.append(features)
                training_labels.append(selmer3_rank)
                print(f"Found high 3-Selmer rank curve: a={a}, b={b}, 3-Selmer rank={selmer3_rank}")
                print(f"Current training data: {training_data}")
                print(f"Current labels: {training_labels}")
    
    # Regenerate interweb plot after each attempt
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
