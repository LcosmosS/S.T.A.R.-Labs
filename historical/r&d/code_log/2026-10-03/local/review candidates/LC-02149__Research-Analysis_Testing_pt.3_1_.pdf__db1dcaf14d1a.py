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


                try:


                    points = E.points(bound=200)


                    non_torsion = [p for p in points if p.order() == 0]


                    if non_torsion:


                        print(f"Found non-torsion points: {non_torsion}")


                        rank = max(1, len(non_torsion))


                    else: