    for a, b in previous_curves:
        result = analyze_curve(a, b, conductor_limit=conductor_limit)
        if len(result) == 16:
            success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size = result
            if success:
                data_tuple = (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size)
                curves_data.append((None, data_tuple))
                with open(csv_file, 'a', newline='') as csv_f:
                    csv_writer = csv.writer(csv_f)
                    csv_writer.writerow(data_tuple)
        gc.collect()
    
    # Generate new curves
    for _ in range(max_attempts):
        a, b = random_fibonacci_pair(fib_numbers, lucas_numbers, high_rank_pairs)
        result = analyze_curve(a, b, conductor_limit=conductor_limit)
        if len(result) == 16:
            success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size = result
            if success:
                data_tuple = (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size)
                curves_data.append((None, data_tuple))
                with open(csv_file, 'a', newline='') as csv_f:
                    csv_writer = csv.writer(csv_f)
                    csv_writer.writerow(data_tuple)
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
            if len(result) == 16:
                success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E_twist, selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size = result
                if success:
                    data_tuple = (a_new, b_new, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size)
                    curves_data.append((f"Twist_d{d}", data_tuple))
                    with open(csv_file, 'a', newline='') as csv_f:
                        csv_writer = csv.writer(csv_f)
                        csv_writer.writerow(data_tuple)
                    if rank >= 3:
                        training_data.append(features)
                        training_labels.append(rank)
                        print(f"Added twisted rank {rank} curve to training data: {features}")
            gc.collect()
    
    # Train classifier
    try:
        X = np.array([row[:4] for row in training_data])
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
    
    # Generate interweb plot
    try:
        interweb_data = []
        for label, (a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, selmer3_rank, log_delta, log_cond, _, _, _, _) in curves_data:
            if omega is not None:
                E = EllipticCurve(QQ, [0, 0, 0, a, b])
                delta = float(E.discriminant())
                conductor = float(E.conductor())
                log_delta = math.log(abs(delta)) if delta != 0 else 0
                log_cond = math.log(abs(conductor)) if conductor > 0 else 0
                cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
                raw_volume = omega * reg * cosmo_scale**3
                denominator = {0: 1e13, 1: 1e15, 2: 5e13, 3: 3e11}.get(rank, 1e13)
                volume = math.log1p(raw_volume) / denominator if raw_volume > 0 else raw_volume / denominator
                interweb_data.append((a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, log_delta, log_cond, volume))
        
        fig = plt.figure(figsize=(14, 12))
        ax = fig.add_subplot(111, projection='3d')
        ranks = [float(x[2]) for x in interweb_data]
        log_deltas = [float(x[8]) for x in interweb_data]
