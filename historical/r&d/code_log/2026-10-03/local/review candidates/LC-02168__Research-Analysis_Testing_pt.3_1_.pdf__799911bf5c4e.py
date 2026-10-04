    weak_bsd_holds = False

    for attempt in range(max_attempts):
        try:
            selmer_rank = E.selmer_rank()
            selmer2_success = True
            two_torsion_rank = 1 if tors_order % 2 == 0 else 0
            rank = E.rank()
            try:
                E.two_descent(verbose=False)
                gens = E.gens()
                descent_rank = len(gens)
                if rank != descent_rank:
                    print(f"Warning: Rank {rank} differs from descent rank {descent_rank}, using {descent_rank}")
                    rank = descent_rank
                rank_success = True
            except:
                print("Two-descent failed, attempting point search")
                points = E.points(bound=200)
                non_torsion = [p for p in points if p.order() == 0]
                if non_torsion:
                    print(f"Found non-torsion points: {non_torsion}")
                    rank = max(1, len(non_torsion))
                else:
                    print("No non-torsion points found, rank likely 0 if Selmer agrees")
                    rank = 0 if selmer_rank == two_torsion_rank else rank
                rank_success = True
            print(f"Algebraic rank: {rank} (independent nodes in cosmic web)")
            print(f"2-Selmer rank: {selmer_rank}")
            try:
                S3 = E.selmer_group(3, [])
                selmer3_rank = len(S3) - 1
                print(f"3-Selmer rank: {selmer3_rank}")
                selmer3_success = True
                if selmer3_rank >= 3:
                    print("Found potential 3-salmer candidate!")
            except Exception as e:
                print(f"Failed to compute 3-Selmer rank: {e}")
            break
        except:
            print(f"Rank computation failed on attempt {attempt + 1}")
            if attempt == max_attempts - 1:
                print("Max attempts reached, skipping curve")
                return False, None, None, None, None, None, None, False

    success = rank_success and selmer2_success and (selmer3_success if require_3selmer else True)
    if success:
        try:
            L = E.lseries()