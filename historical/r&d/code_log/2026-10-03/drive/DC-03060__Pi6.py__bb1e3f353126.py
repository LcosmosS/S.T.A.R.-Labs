def main():
    high_rank_pairs = [(2, 144), (377, 987), (-102, 918), (34, 4181), (17711, 17711), (17711, 46368)]
    max_attempts = 50
    conductor_limit = 1e40  # Increased to reduce skipping
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = f"distortion_free_earth_mapping_nodes_v15_{timestamp}.csv"


    try:
        with open(csv_file, 'w', newline='') as csv_f:
            csv_writer = csv.writer(csv_f)
            csv_writer.writerow(['a', 'b', 'rank', 'leading_coeff', 'omega', 'reg', 'tamagawa', 'weak_bsd_holds', 'selmer3_rank', 'log_delta', 'log_cond', 'longitude', 'latitude', 'elevation', 'size', 'heegner_x', 'heegner_y', 'z'])
    except IOError as e:
        log_print(f"Failed to initialize CSV file {csv_file}: {e}")
        return


    curves_data = []
    all_curves = []
    used_pairs = set()
    total_curves_needed = 542
    batch_size = 3


    fib_indices = list(range(len(fib_numbers)))
    lucas_indices = list(range(len(lucas_numbers)))
    max_attempts_generate = 20000
    attempt = 0
    idx = 0
    scale_factors = [1, 2, 3]


    while len(all_curves) < total_curves_needed and attempt < max_attempts_generate:
      fib_idx = fib_indices[idx % len(fib_indices)]
        lucas_idx = lucas_indices[idx % len(lucas_indices)]
        scale_a = scale_factors[(idx // len(fib_indices)) % len(scale_factors)]
        scale_b = scale_factors[(idx // (len(fib_indices) * len(scale_factors))) % len(scale_factors)]
        variation = (idx // (len(fib_indices) * len(scale_factors) * len(scale_factors))) % 4
        a = fib_numbers[fib_idx] * scale_a
        b = lucas_numbers[lucas_idx] * scale_b
        if variation == 1:
            a = -a
        elif variation == 2:
            b = -b
        elif variation == 3:
            a = -a
            b = -b
        pair = (a, b)
        if pair not in used_pairs:
            used_pairs.add(pair)
            all_curves.append((a, b, fib_idx, lucas_idx, False))
        idx += 1
        attempt += 1


    if len(all_curves) < total_curves_needed:
        log_print(f"Could not generate enough unique curves. Generated {len(all_curves)} out of {total_curves_needed} needed.")
        return


    log_print(f"Generated {len(all_curves)} unique curves")


    # Train ML model to predict curve skipping
    X_train = []
    y_train = []
    for a, b, fib_idx, lucas_idx, is_original in all_curves[:100]:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        delta = E.discriminant()
        conductor = E.conductor()
        tors_order = E.torsion_subgroup().order()
        log_delta = math.log(abs(delta)) if delta != 0 else 0
        log_cond = math.log(float(conductor)) if conductor > 0 else 0
        X_train.append([log_delta, log_cond, tors_order, abs(a), abs(b)])
        y_train.append(1 if conductor > conductor_limit else 0)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    model = LogisticRegression()
    model.fit(X_train_scaled, y_train)
    log_print("Trained ML model for curve skipping prediction")


    n_jobs = 1
    num_batches = (len(all_curves) + batch_size - 1) // batch_size
    plot_data = {'ranks': [], 'heegner_x': [], 'heegner_y': [], 'lat': [], 'lon': [], 'z': [], 'elevation': [], 'phi_adjusted': [], 'lambda_adjusted': []}


    checkpoint_file = f"checkpoint_v15_{timestamp}.csv"
    try:
        with open(checkpoint_file, 'w', newline='') as chk_f:
            chk_writer = csv.writer(chk_f)
            chk_writer.writerow(['batch_idx', 'completed'])
    except IOError as e:
        log_print(f"Failed to initialize checkpoint file {checkpoint_file}: {e}")
        return


    for batch_idx in range(num_batches):
        completed_batches = set()
        try:
            with open(checkpoint_file, 'r') as chk_f:
                chk_reader = csv.reader(chk_f)
                next(chk_reader)
                for row in chk_reader:
                    completed_batches.add(int(row[0]))
        except (IOError, IndexError):
            log_print(f"Error reading checkpoint file {checkpoint_file}, proceeding without checkpoint")
            completed_batches = set()


        if batch_idx in completed_batches:
            log_print(f"Skipping batch {batch_idx+1}/{num_batches} (already processed)")
            continue


        batch_start = batch_idx * batch_size
        batch_end = min(batch_start + batch_size, len(all_curves))
        batch_curves = all_curves[batch_start:batch_end]
        log_print(f"Processing batch {batch_idx+1}/{num_batches} ({batch_start} to {batch_end-1})")


        try:
            import psutil
            process = psutil.Process(os.getpid())
            mem_usage = process.memory_info().rss / 1024**2
            if mem_usage > 6000:
                log_print(f"Memory usage too high ({mem_usage} MB), pausing for garbage collection")
                gc.collect()
                time.sleep(10)
        except ImportError:
            log_print("psutil not available, skipping memory check")


        try:
            results = Parallel(n_jobs=n_jobs, backend="multiprocessing")(
                delayed(analyze_curve)(
                    a, b, fib_idx, lucas_idx, is_original, conductor_limit=conductor_limit, scaler=scaler, model=model
                )
                for a, b, fib_idx, lucas_idx, is_original in batch_curves
            )
        except Exception as e:
            log_print(f"Parallel processing failed for batch {batch_idx+1}: {e}")
            results = []
            for a, b, fib_idx, lucas_idx, is_original in batch_curves:
                result = analyze_curve(a, b, fib_idx, lucas_idx, is_original, conductor_limit=conductor_limit, scaler=scaler, model=model)
                results.append(result)


        for result in results:
            if len(result) != 20:
                continue
            (success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
             selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size, heegner_x,
