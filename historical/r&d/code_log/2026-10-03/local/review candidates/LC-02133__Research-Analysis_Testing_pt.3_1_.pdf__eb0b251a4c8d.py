                descent_rank = len(gens)


                if rank != descent_rank:


                    print(f"Warning: Rank {rank} differs from descent rank {descent_rank}, using {descent_rank}")


                    rank = descent_rank


                rank_success = True


            except:


                print("Two-descent failed, attempting point search")


                try:


                    points = E.points(bound=100)


                    non_torsion = [p for p in points if p.order() == 0]


                    if non_torsion:


                        print(f"Found non-torsion points: {non_torsion}")


                        rank = max(1, rank)


                    else:


                        print("No non-torsion points found, rank likely 0 if Selmer agrees")


                        rank = 0 if selmer_rank == two_torsion_rank else rank


                    rank_success = True


                except:


                    print("Point search failed")