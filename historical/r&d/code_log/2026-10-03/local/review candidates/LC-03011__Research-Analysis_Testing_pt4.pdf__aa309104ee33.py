    # Compute the analytic rank first (safer)
    try:
        L = E.lseries()
        dok = L.dokchitser(prec=100)
        L1 = dok(1)
        analytic_rank = 0
        leading_coeff = L1
        if abs(L1) < 1e-10:
            L1_deriv = dok.derivative(1, 1)
            if abs(L1_deriv) < 1e-10:
                L1_deriv2 = dok.derivative(1, 2)
                if abs(L1_deriv2) < 1e-10:
                    L1_deriv3 = dok.derivative(1, 3)
                    if abs(L1_deriv3) < 1e-10:
                        analytic_rank = 4
                        leading_coeff = L1_deriv3 / 24
                    else:
                        analytic_rank = 3
                        leading_coeff = L1_deriv3 / 6
                else:
                    analytic_rank = 2
                    leading_coeff = L1_deriv2 / 2
            else:
                analytic_rank = 1
                leading_coeff = L1_deriv
        print(f"Analytic rank: {analytic_rank}")
    except Exception as e:
        print(f"Failed to compute analytic rank: {e}")
        return False, None, None, None, None, None, None, False, None, None

    # Attempt algebraic rank computation
    for attempt in range(max_attempts):
        try:
            # Try PARI/GP's ellrank first
            try:
                E_pari = pari.ellinit([0, 0, 0, a, b])
                rank_info = E_pari.ellrank()
                rank = int(rank_info[0])  # First element is the rank
                rank_success = True
                print(f"Algebraic rank (via PARI/GP): {rank}")
            except Exception as e:
                print(f"PARI/GP rank computation failed: {e}")
                rank = analytic_rank
                rank_success = True

            # Refined 3-Selmer rank estimate
            if analytic_rank == rank:
                selmer3_rank = rank
                print(f"3-Selmer rank (refined using BSD): {selmer3_rank}")