                        print("No non-torsion points found, rank likely 0 if Selmer agrees")


                        rank = 0 if selmer_rank == two_torsion_rank else rank


                    rank_success = True


                except:


                    print("Point search failed")


            print(f"Algebraic rank: {rank} (independent nodes in cosmic web)")


            print(f"2-Selmer rank: {selmer_rank}")


            try:


                S3 = E.selmer_group(3, [])


                selmer3_rank = len(S3) - 1


                print(f"3-Selmer rank: {selmer3_rank}")


                selmer3_success = True


            except:


                print("Failed to compute 3-Selmer rank")


            break


        except:


            print(f"Rank computation failed on attempt {attempt + 1}")


            if attempt == max_attempts - 1:


                print("Max attempts reached, skipping curve")