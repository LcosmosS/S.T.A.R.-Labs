                    f.write(f"a={a},b={b},rank={rank},selmer3={selmer3_rank},volume={vol}\n")
            break
        except Exception as e:
            print(f"Rank computation failed on attempt {attempt + 1}: {e}")
            if attempt == max_attempts - 1:
                with open("failed_curves.txt", "a") as f:
                    f.write(f"a={a},b={b},conductor={conductor},reason=rank_failure\n")
                return False, None, None, None, None, None, None, False, None

    success = rank_success and selmer2_success and (selmer3_success if require_3selmer else True)
    if success:
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
                    if abs(L1_deriv2) < 1e-10 and rank >= 3:
                        L1_deriv3 = dok.derivative(1, 3)
                        analytic_rank = 3
                        leading_coeff = L1_deriv3 / 6
                    else:
                        analytic_rank = 2
                        leading_coeff = L1_deriv2 / 2
                else:
                    analytic_rank = 1
                    leading_coeff = L1_deriv
            print(f"Analytic rank: {analytic_rank}")
            print(f"Leading coefficient: {leading_coeff}")
            weak_bsd_holds = (rank == analytic_rank)
            print(f"Weak BSD holds: {weak_bsd_holds}")

            omega = E.period_lattice().real_period(prec=100)