    # Compute the rank
    rank = E.rank()
    print(f"Algebraic rank: {rank}")

    # Compute the L-function and analytic rank
    L = E.lseries()
    # Use Dokchitser to evaluate L(s) and its derivatives with high precision
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

    # Compute BSD invariants for strong BSD
    omega = E.period_lattice().real_period(prec=100)
    reg = E.regulator(prec=100)
    tamagawa = prod(E.tamagawa_numbers())
    sha_order = 1  # Initial hypothesis based on 2-Selmer rank

    # Compute the right-hand side of the strong BSD formula
    rhs = (omega * reg * sha_order * tamagawa) / (tors_order^2)
    print(f"Real period (Omega): {omega}")
    print(f"Regulator: {reg}")
    print(f"Product of Tamagawa numbers: {tamagawa}")
    print(f"Right-hand side of strong BSD (with |Sha(E)| = 1): {rhs}")

    # Verify strong BSD