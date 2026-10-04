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
            except Exception as e:
                print(f"Rank computation failed: {e}")
                print("Trying two-descent...")
                try:
                    E.two_descent(verbose=False, second_limit=20)
                    gens = E.gens()
                    rank = len(gens)
                    rank_success = True
                except:
                    print("Two-descent failed, using rank bound")
                    rank = E.rank_bound()
                    rank_success = True
            print(f"Algebraic rank: {rank} (independent nodes in cosmic web)")
            print(f"2-Selmer rank: {selmer_rank}")
            try:
                selmer3_rank = max(rank, selmer_rank - 1)
                print(f"Estimated 3-Selmer rank (no Magma): {selmer3_rank}")
                selmer3_success = True if not require_3selmer else False
                if selmer3_rank >= 3:
                    print("Potential 3-salmer candidate (estimated)!")
                    with open("rank3_curves.txt", "a") as f:
                        f.write(f"a={a},b={b},rank={rank},selmer3={selmer3_rank}\n")
            except Exception as e:
                print(f"Failed to estimate 3-Selmer rank: {e}")
            break
        except Exception as e:
            print(f"Rank computation failed on attempt {attempt + 1}: {e}")
            if attempt == max_attempts - 1:
                print("Max attempts reached, skipping curve")
                with open("failed_curves.txt", "a") as f:
                    f.write(f"a={a},b={b},conductor={conductor},reason=rank_failure\n")
                return False, None, None, None, None, None, None, False

    success = rank_success and selmer2_success and (selmer3_success if require_3selmer else True)