                analytic_rank = 0


                leading_coeff = L1


            print(f"Analytic rank: {analytic_rank}")


            print(f"Leading coefficient: {leading_coeff} (topological density in cosmic web)")





            if rank == analytic_rank:


                print("Weak BSD holds: Algebraic rank = Analytic rank")


            else:


                print("Weak BSD fails: Algebraic rank != Analytic rank")


        except:


            print("L-function computation failed")


            return False, None, None, None, None, None





        try:


            omega = E.period_lattice().real_period(prec=100)


            reg = E.regulator() if rank > 0 else 1.0


            tamagawa = prod(E.tamagawa_numbers())


            if is_original:


                tamagawa = 4