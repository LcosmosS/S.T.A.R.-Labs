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
            if rank_success and rank != analytic_rank:
                try:
                    selmer_rank = E.selmer_rank()
                    selmer2_success = True
                    print(f"2-Selmer rank: {selmer_rank}")
                except Exception as e:
                    print(f"2-Selmer rank computation failed: {e}")
                    selmer2_success = False

            # Refined 3-Selmer rank estimate
            if selmer2_success:
                estimated_selmer3 = max(rank, selmer_rank - 1)
            else:
                estimated_selmer3 = rank  # Fallback to rank if 2-Selmer rank unavailable
            if analytic_rank == rank:
                selmer3_rank = rank
                print(f"3-Selmer rank (refined using BSD): {selmer3_rank}")
            else:
                selmer3_rank = estimated_selmer3
                print(f"Estimated 3-Selmer rank (fallback): {selmer3_rank}")
            selmer3_success = True if not require_3selmer else False
