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
    print(f"Leading coefficient: {leading_coeff}")

    # Verify weak BSD
    if rank is not None and rank == analytic_rank:
        print("Weak BSD holds: Algebraic rank = Analytic rank")
    else:
        print("Weak BSD fails: Algebraic rank != Analytic rank or computation failed")

    # Compute Heegner points
    D = -19  # Quadratic imaginary field Q(sqrt(-19))
    try:
        P = E.heegner_point(D, c=1)  # Heegner point with conductor 1
        P_Q = P.point()  # Trace to E(Q)
        print(f"Heegner point (traced to Q): {P_Q}")
        order = P_Q.order()
        if order == 0:
            print("Heegner point has infinite order, suggesting rank >= 1")
        else:
            print(f"Heegner point has order {order}, suggesting rank 0 or torsion")
    except ValueError as e:
        print(f"Failed to compute Heegner point: {e}")

    # Compute 2-Selmer rank
    try:
        selmer_rank = E.selmer_rank()
        two_torsion_rank = 1 if tors_order % 2 == 0 else 0
        sha_two_rank = selmer_rank - rank - two_torsion_rank if rank is not None else None
        print(f"2-Selmer rank: {selmer_rank}")
        print(f"Rank of Sha(E)[2]: {sha_two_rank}")
        if sha_two_rank == 0:
            print("Sha(E)[2] = 0, suggesting |Sha(E)| is odd or 1")
        elif sha_two_rank is not None:
            print(f"|Sha(E)[2]| = 2^{sha_two_rank}")
    except:
        print("Failed to compute 2-Selmer rank")

    # Compute BSD invariants for strong BSD
    try:
        omega = E.period_lattice().real_period(prec=100)