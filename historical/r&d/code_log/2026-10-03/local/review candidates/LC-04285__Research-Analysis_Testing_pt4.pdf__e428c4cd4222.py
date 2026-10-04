        return False, None, None, None, None, None, None, False, None

    delta = E.discriminant()
    conductor = E.conductor()
    tors_order = E.torsion_subgroup().order()
    print(f"Discriminant: {delta}")
    print(f"Conductor: {conductor} = {factor(conductor)}")
    print(f"Torsion order: {tors_order}")

    if conductor > conductor_limit and not is_original:
        print(f"Conductor too large (> {conductor_limit}), skipping curve")
        with open("failed_curves.txt", "a") as f:
            f.write(f"a={a},b={b},conductor={conductor},reason=too_large\n")
        return False, None, None, None, None, None, None, False, None

    rank_success = False
    selmer2_success = False
    selmer3_success = False
    rank = None
    selmer_rank = None
    selmer3_rank = None
    leading_coeff = None
    omega = None
    reg = None
    tamagawa = None
    weak_bsd_holds = False

    # Compute the analytic rank first (safer)
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
