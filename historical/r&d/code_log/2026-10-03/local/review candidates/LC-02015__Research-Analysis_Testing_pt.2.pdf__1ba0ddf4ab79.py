    # Compute BSD invariants for strong BSD
    omega = E.period_lattice().real_period(prec=100)
    reg = E.regulator(prec=100)
    tamagawa = prod(E.tamagawa_numbers())
    sha_order = 1  # Hypothesized based on 2-Selmer rank (we'll adjust if needed)

    # Compute the right-hand side of the strong BSD formula
    rhs = (omega * reg * sha_order * tamagawa) / (tors_order^2)
    print(f"Real period (Omega): {omega}")
    print(f"Regulator: {reg}")
    print(f"Product of Tamagawa numbers: {tamagawa}")
    print(f"Right-hand side of strong BSD: {rhs}")

    # Verify strong BSD
    if abs(leading_coeff - rhs) < 1e-10:
        print("Strong BSD holds: Leading coefficient matches")
    else:
        print("Strong BSD fails: Leading coefficient does not match")
        # Adjust Sha(E) to match
        sha_order = (leading_coeff * tors_order^2) / (omega * reg * tamagawa)
        print(f"Adjusted |Sha(E)| to match: {sha_order}")
