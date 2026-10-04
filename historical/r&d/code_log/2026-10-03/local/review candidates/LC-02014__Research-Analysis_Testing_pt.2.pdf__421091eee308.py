# Loop over each pair to construct and analyze the curve
for n1, n2 in pairs:
    a = fibonacci(n1)
    b = fibonacci(n2)
    print(f"\nCurve with a = F_{n1} = {a}, b = F_{n2} = {b}: y^2 = x^3 + {a}x + {b}")

    # Define the elliptic curve
    E = EllipticCurve(QQ, [a, b])

    # Compute the discriminant
    delta = E.discriminant()
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
    print(f"Algebraic rank: {rank}")

    # Compute the L-function and analytic rank
    L = E.lseries()
    L1 = L(1, prec=100)
    if L1.abs() < 1e-10:  # Check if L(1) is approximately 0
        L1_deriv = L.dokchitser(prec=100).derivative(1, 1)
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
