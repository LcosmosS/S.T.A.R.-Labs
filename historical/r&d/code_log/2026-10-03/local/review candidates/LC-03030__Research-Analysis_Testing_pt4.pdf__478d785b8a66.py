    try:

        L = E.lseries()

        dok = L.dokchitser(prec=100)

        L1 = dok(1)

        analytic_rank = 0

        leading_coeff = L1
        if abs(L1) < 1e-10:

            L1_deriv = dok.derivative(1, 1)

            if abs(L1_deriv) < 1e-10:

                L1_deriv2 = dok.derivative(1, 2)

                if abs(L1_deriv2) < 1e-10:

                    L1_deriv3 = dok.derivative(1, 3)

                    if abs(L1_deriv3) < 1e-10:

                        analytic_rank = 4

                        leading_coeff = L1_deriv3 / 24

                    else:

                        analytic_rank = 3

                        leading_coeff = L1_deriv3 / 6

                else:

                    analytic_rank = 2

                    leading_coeff = L1_deriv2 / 2

            else:

                analytic_rank = 1

                leading_coeff = L1_deriv

        print(f"Analytic rank: {analytic_rank}")

    except Exception as e:
        print(f"Failed to compute analytic rank: {e}")

        return False, None, None, None, None, None, None, False, None, None



    # Attempt algebraic rank computation