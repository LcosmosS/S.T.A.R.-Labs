                        analytic_rank = 1
                # Refine the estimate: 3-Selmer rank is between rank and 2-Selmer rank
                # If analytic rank matches algebraic rank (BSD holds), use it to bound
                estimated_selmer3 = max(rank, selmer_rank - 1)
                if analytic_rank == rank:
                    # If BSD holds, 3-Selmer rank should be close to algebraic rank
                    selmer3_rank = max(rank, min(selmer_rank, analytic_rank + 1))
                else:
                    selmer3_rank = estimated_selmer3
                print(f"Estimated 3-Selmer rank (refined without Magma): {selmer3_rank}")
                selmer3_success = True if not require_3selmer else False

            if selmer3_rank >= 3:
                print("Potential 3-Selmer candidate!")
                with open("rank3_curves.txt", "a") as f:
                    vol = omega * reg * (VIRGO_DISTANCE / (omega * SQRT_KAPPA))**3 / 3e11 if omega and
