    selmer_rank = None
    selmer3_rank = None
    leading_coeff = None
    omega = None
    reg = None
    tamagawa = None
    weak_bsd_holds = False

    for attempt in range(max_attempts):
        try:
            selmer_rank = E.selmer_rank()
            selmer2_success = True
            try:
                rank = E.rank(only_use_mwrank=False)
                rank_success = True
            except Exception:
                print("Trying two-descent...")
                E.two_descent(verbose=False, second_limit=20)
                gens = E.gens()
                rank = len(gens)
                rank_success = True
            print(f"Algebraic rank: {rank}")
            print(f"2-Selmer rank: {selmer_rank}")

            # Attempt to compute 3-Selmer rank using SageMath's three_descent
            try:
                selmer3_result = E.three_descent(verbose=False)
                selmer3_group = selmer3_result[0]  # The 3-Selmer group
                selmer3_rank = selmer3_group.rank()
                selmer3_success = True
                print(f"Computed 3-Selmer rank: {selmer3_rank}")
            except Exception as e:
                print(f"3-descent failed: {e}")
                # Fallback: Refine the estimate using analytic rank and 2-Selmer rank
                # First, compute the analytic rank
                L = E.lseries()
                dok = L.dokchitser(prec=100)
                L1 = dok(1)
                analytic_rank = 0
                if abs(L1) < 1e-10:
                    L1_deriv = dok.derivative(1, 1)
                    if abs(L1_deriv) < 1e-10:
                        L1_deriv2 = dok.derivative(1, 2)
                        if abs(L1_deriv2) < 1e-10 and rank >= 3:
                            L1_deriv3 = dok.derivative(1, 3)
                            analytic_rank = 3
                        else:
                            analytic_rank = 2
                    else: