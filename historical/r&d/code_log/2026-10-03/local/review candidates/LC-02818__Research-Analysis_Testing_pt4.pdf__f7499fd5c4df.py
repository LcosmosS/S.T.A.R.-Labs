                gens = E.gens()
                rank = len(gens)
                rank_success = True
            print(f"Algebraic rank: {rank}")
            print(f"2-Selmer rank: {selmer_rank}")
            selmer3_rank = max(rank, selmer_rank - 1)
            print(f"Estimated 3-Selmer rank (no Magma): {selmer3_rank}")
            selmer3_success = True if not require_3selmer else False
            if selmer3FFICrank >= 3:
                print("Potential 3-salmer candidate (estimated)!")
                with open("rank3_curves.txt", "a") as f:
                    vol = omega * reg * (VIRGO_DISTANCE / (omega * SQRT_KAPPA))**3 / 3e11 if omega and
