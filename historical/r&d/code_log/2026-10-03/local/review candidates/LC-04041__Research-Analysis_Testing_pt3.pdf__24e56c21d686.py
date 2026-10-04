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
    omega = E.period_lattice().real_period(prec=50)  # Reduced precision
    if rank == 0:
        reg = 1.0
    else:
        reg = E.regulator()
    tamagawa = prod(E.tamagawa_numbers())
    sha_order = 1  # Initial hypothesis

    # Compute the right-hand side of the strong BSD formula
    rhs = (omega * reg * sha_order * tamagawa) / (tors_order^2)
    print(f"Real period (Omega): {omega}")
    print(f"Regulator: {reg}")
    print(f"Product of Tamagawa numbers: {tamagawa}")
    print(f"Right-hand side of strong BSD (with |Sha(E)| = 1): {rhs}")

    # Verify strong BSD
    if abs(leading_coeff - rhs) < 1e-10:
        print("Strong BSD holds: Leading coefficient matches with |Sha(E)| = 1")
    else:
        print("Strong BSD fails: Leading coefficient does not match with |Sha(E)| = 1")
        sha_order = (leading_coeff * tors_order^2) / (omega * reg * tamagawa)
        print(f"Adjusted |Sha(E)| to match: {sha_order}")
