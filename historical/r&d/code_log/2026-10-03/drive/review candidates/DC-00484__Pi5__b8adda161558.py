    try:
        import psutil
        process = psutil.Process(os.getpid())
        mem_usage = process.memory_info().rss / 1024**2
        dynamic_limit = conductor_limit * (1 - mem_usage / 8000)
        dynamic_limit = max(dynamic_limit, 1e10)
        log_print(f"Dynamic conductor limit: {dynamic_limit}")
    except ImportError:
        dynamic_limit = conductor_limit
        log_print("psutil not available, using static conductor limit")


    if conductor > dynamic_limit:
        log_print(f"Conductor {conductor} exceeds dynamic limit {dynamic_limit}, performing partial analysis")
        heegner_x = heegner_y = 0
    else:
        if conductor > conductor_limit:
            log_print(f"Conductor too large (> {conductor_limit}), skipping curve")
            return (success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
                    selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size,
                    heegner_x, heegner_y, z, phi_adjusted, lambda_adjusted)
