    selmer3_rank = None





    for attempt in range(max_attempts):


        try:


            selmer_rank = E.selmer_rank()


            selmer2_success = True


            two_torsion_rank = 1 if tors_order % 2 == 0 else 0


            rank_bound = selmer_rank - two_torsion_rank


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