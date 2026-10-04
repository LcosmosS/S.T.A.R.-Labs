                print("Trying two-descent with higher second_limit...")
                try:
                    E.two_descent(verbose=False, second_limit=20)
                    gens = E.gens()
                    rank = len(gens)
                    rank_success = True
                except Exception as e:
                    print(f"Two-descent failed: {e}. Retrying with only_use_mwrank=False...")
                    try:
                        rank = E.rank(only_use_mwrank=False)
                        rank_success = True
                    except Exception as e:
                        print(f"Rank computation failed: {e}")
                        rank_success = False
                        break
            print(f"Algebraic rank: {rank}")
            print(f"2-Selmer rank: {selmer_rank}")

            # Compute analytic rank to refine 3-Selmer rank estimate
            L = E.lseries()
            dok = L.dokchitser(prec=100)
            L1 = dok(1)
            analytic_rank = 0
            leading_coeff = L1
            if abs(L1) < 1e-10:
                L1_deriv = dok.derivative(1, 1)
                if abs(L1_deriv) < 1e-10:
                    L1_deriv2 = dok.derivative(1, 2)
                    if abs(L1_deriv2) < 1e-10 and rank >= 3:
                        L1_deriv3 = dok.derivative(1, 3)
                        analytic_rank = 3
                        leading_coeff = L1_deriv3 / 6
                    else:
                        analytic_rank = 2
                        leading_coeff = L1_deriv2 / 2
                else:
                    analytic_rank = 1
                    leading_coeff = L1_deriv
            print(f"Analytic rank: {analytic_rank}")

            # Refined 3-Selmer rank estimate
            # Since strong BSD holds with |Sha(E)| = 1, assume Ш(E/Q)[3] is trivial
            # Thus, 3-Selmer rank should equal algebraic rank if BSD holds
            estimated_selmer3 = max(rank, selmer_rank - 1)
            if analytic_rank == rank:
                # BSD holds, so 3-Selmer rank is likely equal to algebraic rank
                selmer3_rank = rank
                print(f"3-Selmer rank (refined using BSD): {selmer3_rank}")
            else:
