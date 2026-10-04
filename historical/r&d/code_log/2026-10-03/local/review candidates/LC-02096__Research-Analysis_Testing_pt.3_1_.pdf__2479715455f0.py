            print(f"Rank computation failed on attempt {attempt + 1}")

            if attempt == max_attempts - 1:

                print("Max attempts reached, skipping curve")

                return False, None



    # Relaxed success: rank and 2-Selmer required, 3-Selmer optional

    success = rank_success and selmer2_success

    if success:
        try:

            L = E.lseries()

            dok = L.dokchitser(prec=100)

            L1 = dok(1)

            if abs(L1) < 1e-10:

                try:

                    L1_deriv = dok.derivative(1, 1)

                    if abs(L1_deriv) < 1e-10:

                        L1_deriv2 = dok.derivative(1, 2)

                        analytic_rank = 2

                        leading_coeff = L1_deriv2 / 2

                    else:

                        analytic_rank = 1

                        leading_coeff = L1_deriv

                except:

                    analytic_rank = 2

                    leading_coeff = 0

            else:

                analytic_rank = 0
                leading_coeff = L1

            print(f"Analytic rank: {analytic_rank}")

            print(f"Leading coefficient: {leading_coeff} (topological density in cosmic web)")



            if rank == analytic_rank: