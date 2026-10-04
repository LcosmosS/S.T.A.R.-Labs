                # Fallback to previous estimate if BSD doesn't hold
                selmer3_rank = estimated_selmer3
                print(f"Estimated 3-Selmer rank (fallback): {selmer3_rank}")
            selmer3_success = True if not require_3selmer else False

            if selmer3_rank >= 3:
                print("Potential 3-Selmer candidate!")
                with open("rank3_curves.txt", "a") as f:
                    vol = omega * reg * (VIRGO_DISTANCE / (omega * SQRT_KAPPA))**3 / 3e11 if omega and
