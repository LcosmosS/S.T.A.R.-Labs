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
        return False, None, None, None, None, None, None, False, None

    # Attempt algebraic rank computation
    for attempt in range(max_attempts):
        try:
            selmer_rank = E.selmer_rank()
            selmer2_success = True
            try:
                rank = E.rank(only_use_mwrank=True)  # Use mwrank first for stability
                rank_success = True
            except Exception as e:
                print("Trying two-descent with higher second_limit...")
                try:
                    E.two_descent(verbose=False, second_limit=20)
                    gens = E.gens()
                    rank = len(gens)
                    rank_success = True
                except Exception as e:
                    print(f"Two-descent failed: {e}. Falling back to analytic rank...")
                    rank = analytic_rank  # Fallback to analytic rank
                    rank_success = True
                    selmer2_success = False  # Can't compute 2-Selmer rank
            print(f"Algebraic rank: {rank}")
            if selmer2_success:
                print(f"2-Selmer rank: {selmer_rank}")

            # Refined 3-Selmer rank estimate
            if selmer2_success:
                estimated_selmer3 = max(rank, selmer_rank - 1)
