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
            # Try PARI/GP's ellrank first
            try:
                E_pari = pari.ellinit([0, 0, 0, a, b])
                rank_info = E_pari.ellrank()
                rank = int(rank_info[0])  # First element is the rank
                rank_success = True
                print(f"Algebraic rank (via PARI/GP): {rank}")
            except Exception as e:
                print(f"PARI/GP rank computation failed: {e}")
                # Try transforming the curve to reduce coefficients
                u = 1 / math.sqrt(abs(a)) if abs(a) > 1 else 1
                a_new, b_new = transform_curve(a, b, u)
                print(f"Transforming curve with u={u}: y² = x³ + {a_new}x + {b_new}")
                try:
                    E_transformed = EllipticCurve(QQ, [0, 0, 0, a_new, b_new])
                    rank = E_transformed.rank(pari_effort=10)  # Increase precision
                    rank_success = True
                    print(f"Algebraic rank (transformed curve): {rank}")
                except Exception as e:
                    print(f"Rank computation on transformed curve failed: {e}")
                    # Fallback to mwrank with increased effort
                    try:
                        rank = E.rank(pari_effort=10)
                        rank_success = True
                        print(f"Algebraic rank (mwrank with high effort): {rank}")
                    except Exception as e:
                        print(f"mwrank failed: {e}. Falling back to analytic rank...")
                        rank = analytic_rank
                        rank_success = True

            # Compute 2-Selmer rank if possible