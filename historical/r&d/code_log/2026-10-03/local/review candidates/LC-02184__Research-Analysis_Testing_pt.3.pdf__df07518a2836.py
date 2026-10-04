    print(f"Leading coefficient L^{(r)}(E, 1): {leading_coeff}")

    # Verify weak BSD
    if rank == analytic_rank:
        print("Weak BSD holds: Algebraic rank = Analytic rank")
    else:
        print("Weak BSD fails: Algebraic rank != Analytic rank")

    # Use Heegner points to construct rational points (Euler system approach)
    # Choose a discriminant D for the quadratic imaginary field K = Q(sqrt(D))
    D = -19  # Satisfies Heegner hypothesis for all curves
    try:
        # Compute a Heegner point with conductor 1
        P_K = E.heegner_point(D, 1)  # Heegner point in E(K)
        P = P_K.trace_to_rational()  # Trace to E(Q)
        print(f"Heegner point (traced to Q): {P.xy()}")
        # Check if the point has infinite order
        if P.order() == 0:
            print("Heegner point has infinite order, suggesting rank >= 1")
        else:
            print(f"Heegner point has order {P.order()}, suggesting rank 0 or torsion")
    except ValueError as e:
        print(f"Failed to compute Heegner point: {e}")

    # Compute the 2-Selmer rank using two_descent()
    try:
        E.two_descent(verbose=False)
        selmer_rank = E.selmer_rank()  # Use selmer_rank() if available
        print(f"2-Selmer rank: {selmer_rank}")
        # Selmer rank = rank + rank of E(Q)[2] + rank of Sha(E)[2]
        two_torsion_rank = 1 if tors_order % 2 == 0 else 0  # Approximate
        sha_two_rank = selmer_rank - rank - two_torsion_rank
        print(f"Rank of Sha(E)[2]: {sha_two_rank}")
        if sha_two_rank == 0:
            print("Sha(E)[2] = 0, suggesting |Sha(E)| is odd or 1")
        else:
            print(f"|Sha(E)[2]| = 2^{sha_two_rank}")
    except ValueError as e:
        print(f"Failed to compute 2-Selmer rank: {e}")

    # Compute BSD invariants for strong BSD
    omega = E.period_lattice().real_period(prec=100)
    if rank == 0:
        reg = 1.0
    else:
        reg = E.regulator()
    tamagawa = prod(E.tamagawa_numbers())
    sha_order = 1  # Initial hypothesis
