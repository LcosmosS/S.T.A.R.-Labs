    for a, b in previous_curves:
        result = analyze_curve(a, b, conductor_limit=conductor_limit)
        if len(result) == 10:
            success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank = result
            if success:
                curves_data.append((None, (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank, features)))
        gc.collect()
    
    # Generate new curves
    for _ in range(max_attempts):
        a, b = random_fibonacci_pair(fib_numbers, lucas_numbers, high_rank_pairs)
        result = analyze_curve(a, b, conductor_limit=conductor_limit)
        if len(result) == 10:
            success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank = result
            if success:
                curves_data.append((None, (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank, features)))
                if rank >= 3:
                    training_data.append(features)
                    training_labels.append(rank)
                    print(f"Added new rank {rank} curve to training data: {features}")
        gc.collect()
    
    # Quadratic twists for high-rank candidates
    twist_primes = [2, 3, 5, 7]
    for a, b in high_rank_pairs:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        for d in twist_primes:
            E_twist = quadratic_twist(E, d)
            a_new = E_twist.a4()
            b_new = E_twist.a6()
            print(f"\nTwisting curve (a={a}, b={b}) with d={d}")
            result = analyze_curve(a_new, b_new, conductor_limit=conductor_limit)
            if len(result) == 10:
                success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E_twist, selmer3_rank = result
                if success:
                    curves_data.append((f"Twist_d{d}", (a_new, b_new, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E_twist, selmer3_rank, features)))
                    if rank >= 3:
                        training_data.append(features)
                        training_labels.append(rank)
                        print(f"Added twisted rank {rank} curve to training data: {features}")
            gc.collect()
    
    # Train classifier
    try:
        X = np.array([row[:4] for row in training_data])  # Exclude torsion order for simplicity
        y = np.array(training_labels)
        if len(set(y)) >= 2 and len(X) >= 5:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            clf = LogisticRegression(class_weight='balanced')
            clf.fit(X_scaled, y)
            print("Classifier trained successfully")
        else:
            print("Insufficient data or labels for classifier training")
    except Exception as e:
        print(f"Failed to train classifier: {e}")
    
    # Generate improved cosmic interweb plot
    try:
        interweb_data = []
        for label, (a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, _, features) in curves_data:
            if omega is not None:
                delta = float(E.discriminant())
                conductor = float(E.conductor())
                log_delta = math.log(abs(delta)) if delta != 0 else 0
                log_cond = math.log(abs(conductor)) if conductor != 0 else 0
                cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
                raw_volume = omega * reg * cosmo_scale**3
                denominator = {0: 1e13, 1: 1e15, 2: 5e13, 3: 3e11}.get(rank, 1e13)
                volume = math.log1p(raw_volume) / denominator if raw_volume > 0 else raw_volume / denominator
                interweb_data.append((a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, log_delta, log_cond, volume))
        
        fig = plt.figure(figsize=(14, 12))
        ax = fig.add_subplot(111, projection='3d')
        ranks = [float(x[2]) for x in interweb_data]
        log_deltas = [float(x[8]) for x in interweb_data]
        log_conds = [float(x[9]) for x in interweb_data]
        volumes = [float(x[10]) for x in interweb_data]
        sizes = [float(max(x[3] * 100, 1e-6)) for x in interweb_data]
        
        # Color by rank for clarity
        colors = ['k' if r == 0 else 'g' if r == 1 else 'b' if r == 2 else 'r' for r in ranks]
        scatter = ax.scatter(log_deltas, log_conds, ranks, s=sizes, c=colors, alpha=0.7)
        
        # Add Virgo Supercluster marker
        virgo_rank = 3
        largest_rank3 = max([x for x in interweb_data if x[2] == 3], key=lambda x: x[10], default=None)
        if largest_rank3:
            virgo_log_delta = largest_rank3[8] + 0.5
            virgo_log_cond = largest_rank3[9] + 0.5
        else:
            virgo_log_delta, virgo_log_cond = 23.0, 22.0
        ax.scatter([virgo_log_delta], [virgo_log_cond], [virgo_rank], s=200, c='green', marker='*', label='Virgo Supercluster')
        ax.text(virgo_log_delta + 0.5, virgo_log_cond + 0.5, virgo_rank + 0.1, 'Virgo Supercluster', size=10, color='green')
        
        # Plot filaments with refined weights
        for i, (a, b, rank, _, _, reg, _, _, log_delta, log_cond, _) in enumerate(interweb_data):
            for j in range(i + 1, len(interweb_data)):
                reg_diff = abs(interweb_data[i][5] - interweb_data[j][5])
                if reg_diff < 5000:  # Tighter threshold for clearer filaments
                    weight = 1 / (1 + reg_diff / 100)
                    if weight > 0.7:  # Higher threshold for visibility
                        ax.plot([log_deltas[i], log_deltas[j]], [log_conds[i], log_conds[j]], [ranks[i], ranks[j]], 'b-', alpha=0.5 * weight, linewidth=0.7 * weight)
            if rank >= 2:
                color = 'red' if rank == 3 else 'blue'
                offset = 0.5 if log_delta > 20 else -0.5
                ax.text(log_delta + offset, log_cond + offset, rank + 0.1, f'({a},{b})', size=8, color=color)
        
        ax.set_xlabel('Log(|Discriminant|)')
        ax.set_ylabel('Log(|Conductor|)')
        ax.set_zlabel('Rank')
        ax.set_title('Cosmic Interweb: Nodes, Weighted Filaments, and Virgo Supercluster Marker')
        ax.grid(True)
        ax.legend()
        plt.savefig("interweb_enhanced_with_virgo.png")
        plt.close()
        print("Enhanced cosmic interweb plot saved as interweb_enhanced_with_virgo.png")
        
        # Save interweb data for empirical comparison
        with open('interweb_nodes.txt', 'w') as f:
            for data in interweb_data:
                f.write(str(data) + '\n')
        print("Interweb data saved to interweb_nodes.txt")
    except Exception as e:
        print(f"Failed to generate interweb plot: {e}")
    
    print(f"\nFinal training data: {training_data}")
    print(f"Final labels: {training_labels}")


if __name__ == '__main__':
    main()
