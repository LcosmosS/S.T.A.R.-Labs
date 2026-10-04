    print(f"Discriminant: {delta}")
    if delta == 0:
        print("Not an elliptic curve (singular). Skipping.")
        continue

    # Compute the conductor
    conductor = E.conductor()
    print(f"Conductor: {conductor}")

    # Compute the torsion subgroup
    tors = E.torsion_subgroup()
    tors_order = tors.order()
    print(f"Torsion subgroup order: {tors_order}")

    # Compute the rank
    rank = E.rank()
    print(f"Algebraic rank (via SageMath): {rank}")

    # Compute the L-function and analytic rank
    L = E.lseries()
    L_dok = L.dokchitser(prec=100)
    L1 = L_dok(1)  # Evaluate L(1)
    if abs(L1) < 1e-10:  # Check if L(1) is approximately 0
        L1_deriv = L_dok.derivative(1, 1)  # Compute L'(1)
        if abs(L1_deriv) < 1e-10:  # Check if L'(1) is approximately 0
            L1_deriv2 = L_dok.derivative(1, 2)  # Compute L''(1)
            if abs(L1_deriv2) < 1e-10:
                analytic_rank = 3  # Continue for higher ranks if needed
                leading_coeff = L1_deriv2 / 2  # Leading term is L''(1)/2!
            else:
                analytic_rank = 2
                leading_coeff = L1_deriv2 / 2
        else:
            analytic_rank = 1
            leading_coeff = L1_deriv
    else:
        analytic_rank = 0
        leading_coeff = L1
    print(f"Analytic rank: {analytic_rank}")
    print(f"Leading coefficient L^{(r)}(E, 1): {leading_coeff}")

    # Verify weak BSD
    if rank == analytic_rank:
        print("Weak BSD holds: Algebraic rank = Analytic rank")
    else:
        print("Weak BSD fails: Algebraic rank != Analytic rank")

    # Use Heegner points to construct rational points (Euler system approach)
    # Choose a discriminant D for the quadratic imaginary field K = Q(sqrt(D))