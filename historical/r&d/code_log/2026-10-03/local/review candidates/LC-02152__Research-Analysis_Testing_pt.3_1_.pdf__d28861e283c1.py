                        else:


                            analytic_rank = 2


                            leading_coeff = L1_deriv2 / 2


                    else:


                        analytic_rank = 1


                        leading_coeff = L1_deriv


                except:


                    analytic_rank = max(2, rank)


                    leading_coeff = 0


            print(f"Analytic rank: {analytic_rank}")


            print(f"Leading coefficient: {leading_coeff} (topological density in cosmic web)")





            weak_bsd_holds = (rank == analytic_rank)


            if weak_bsd_holds:


                print("Weak BSD holds: Algebraic rank = Analytic rank")


            else:


                print("Weak BSD fails: Algebraic rank != Analytic rank")


        except:


            print("L-function computation failed")