            except:


                print("Failed to compute 3-Selmer rank")


            break


        except:


            print(f"Rank computation failed on attempt {attempt + 1}")


            if attempt == max_attempts - 1:


                print("Max attempts reached, skipping curve")


                return False, None, None





    # Success criteria


    success = rank_success and selmer2_success and (selmer3_success if require_3selmer else True)


    if success:


        try:


            L = E.lseries()


            dok = L.dokchitser(prec=100)


            L1 = dok(1)


            if abs(L1) < 1e-10:


                try:


                    L1_deriv = dok.derivative(1, 1)