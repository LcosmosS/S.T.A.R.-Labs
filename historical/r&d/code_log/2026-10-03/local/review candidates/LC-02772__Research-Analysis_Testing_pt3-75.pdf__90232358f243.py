    selmer2_success = False
    selmer3_success = False
    rank = None
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
            selmer3_rank = max(rank, selmer_rank - 1)
            print(f"Estimated 3-Selmer rank (no Magma): {selmer3_rank}")
            selmer3_success = True if not require_3selmer else False
            if selmer3_rank >= 3:
                print("Potential 3-salmer candidate (estimated)!")
                with open("rank3_curves.txt", "a") as f:
                    vol = omega * reg * (VIRGO_DISTANCE / (omega * SQRT_KAPPA))**3 / 1.5e13 if omega
