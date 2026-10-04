            else:
                estimated_selmer3 = rank  # Fallback to rank if 2-Selmer rank unavailable
            if analytic_rank == rank:
                # Weak BSD holds, so 3-Selmer rank is likely equal to rank
                selmer3_rank = rank
                print(f"3-Selmer rank (refined using BSD): {selmer3_rank}")
            else:
                selmer3_rank = estimated_selmer3
                print(f"Estimated 3-Selmer rank (fallback): {selmer3_rank}")
            selmer3_success = True if not require_3selmer else False

            if selmer3_rank >= 3:
                print("Potential 3-Selmer candidate!")
                with open("rank3_curves.txt", "a") as f:
                    vol = omega * reg * (VIRGO_DISTANCE / (omega * SQRT_KAPPA))**3 / 3e11 if omega and
