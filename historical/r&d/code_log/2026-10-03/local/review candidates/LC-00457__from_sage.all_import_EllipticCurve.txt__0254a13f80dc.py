    a1, a2, a3, a4, a6 = coeffs
    
    # SymPy for symbolic curve representation
    x, y = symbols('x y')
    a4_sym, a6_sym = sympify(a4), sympify(a6)
    curve_eq = Eq(y**2, x**3 + a4_sym*x + a6_sym)
    print(f"Curve equation: {curve_eq}")

    # Create SageMath EllipticCurve
    try:
        E = EllipticCurve(coeffs)
    except Exception as e:
        print(f"Failed to create elliptic curve: {e}")
        return

    # Compute the discriminant
    delta = E.discriminant()
    print(f"Discriminant: {delta}")
    if delta == 0:
        print("Not an elliptic curve (singular). Skipping.")
        return

    # Compute the conductor
    try:
        N = E.conductor()
        print(f"Conductor: {N}")
    except Exception as e:
        print(f"Failed to compute conductor: {e}")
        N = "Unknown"

    # Compute the torsion subgroup
    try:
        tors = E.torsion_subgroup()
        tors_order = tors.order()
        print(f"Torsion subgroup order: {tors_order}")
    except Exception as e:
        print(f"Failed to compute torsion subgroup: {e}")
        tors_order = "Unknown"

    # Compute the algebraic rank
    try:
        rank = E.rank()
        print(f"Algebraic rank: {rank}")
    except Exception as e:
        print(f"Failed to compute rank: {e}")
        rank = "Unknown"

    # Compute the L-function and analytic rank
    try:
        L = E.lseries()  # Use EllipticCurve's lseries method
        Lval = L(1)
        if abs(Lval) < 1e-10:
            Lderiv = L.derivative(1, 1)
            if abs(Lderiv) < 1e-10:
                Lderiv2 = L.derivative(1, 2)
                if abs(Lderiv2) < 1e-10:
                    analytic_rank = 3
                    leading_coeff = Lderiv2 / 2
                else:
                    analytic_rank = 2
                    leading_coeff = Lderiv2 / 2
            else:
                analytic_rank = 1
                leading_coeff = Lderiv
        else:
            analytic_rank = 0
            leading_coeff = Lval
        print(f"Analytic rank: {analytic_rank}")
        print(f"Leading coefficient L^(r)(E, 1): {leading_coeff}")
    except Exception as e:
        print(f"Failed to compute L-function: {e}")
        analytic_rank = "Unknown"
        leading_coeff = "Unknown"

    # Verify weak BSD
    if rank != "Unknown" and analytic_rank != "Unknown":
        if rank == analytic_rank:
            print("Weak BSD holds: Algebraic rank = Analytic rank")
        else:
            print("Weak BSD fails: Algebraic rank != Analytic rank")
    else:
        print("Weak BSD cannot be verified due to unknown rank(s).")

    # Heegner points (using D = -19 as in MAGMA)
    D = -19
    try:
        P_K = E.heegner_point(D, 1)  # Heegner point with conductor 1
        P = P_K.point()  # Trace to E(Q)
        print(f"Heegner point (traced to Q): {P}")
        # Check if the point has infinite order
        order = P.order()
        if order == 0:
            print("Heegner point has infinite order, suggesting rank >= 1")
        else:
            print(f"Heegner point has order {order}, suggesting rank 0 or torsion")
    except Exception as e:
        print(f"Failed to compute Heegner point: {e}")

    # Compute the 2-Selmer group
    try:
        S2 = E.two_selmer_group()
        selmer_rank = S2.rank()  # SageMath returns the rank directly
        print(f"2-Selmer rank: {selmer_rank}")
        # Selmer rank = rank + rank of E(Q)[2] + rank of Sha(E)[2]
        two_torsion_rank = 1 if tors_order % 2 == 0 else 0
        sha_two_rank = selmer_rank - (rank if rank != "Unknown" else 0) - two_torsion_rank
        print(f"Rank of Sha(E)[2]: {sha_two_rank}")
        if sha_two_rank == 0:
            print("Sha(E)[2] = 0, suggesting |Sha(E)| is odd or 1")
        else:
            print(f"|Sha(E)[2]| = {2^sha_two_rank}")
    except Exception as e:
        print(f"Failed to compute 2-Selmer group: {e}")

    # Compute BSD invariants for strong BSD
    try:
        omega = E.period_lattice().omega()
        if rank == 0 or rank == "Unknown":
            reg = R(1.0)
        else:
            reg = E.regulator()  # Use EllipticCurve's regulator method
        tamagawa = prod(TamagawaNumber(E, p) for p in E.conductor().prime_factors())
        sha_order = R(1)  # Initial hypothesis

        # Right-hand side of strong BSD
        rhs = (omega * reg * sha_order * tamagawa) / (tors_order^2 if tors_order != "Unknown" else 1)
        print(f"Real period (Omega): {omega}")
        print(f"Regulator: {reg}")
        print(f"Product of Tamagawa numbers: {tamagawa}")
        print(f"Right-hand side of strong BSD (with |Sha(E)| = 1): {rhs}")

        # Verify strong BSD
        if leading_coeff != "Unknown" and abs(leading_coeff - rhs) < 1e-10:
            print("Strong BSD holds: Leading coefficient matches with |Sha(E)| = 1")
        else:
            print("Strong BSD fails: Leading coefficient does not match with |Sha(E)| = 1")
            if leading_coeff != "Unknown" and tors_order != "Unknown":
                sha_order = (leading_coeff * tors_order^2) / (omega * reg * tamagawa)
                print(f"Adjusted |Sha(E)| to match: {sha_order}")
    except Exception as e:
        print(f"Failed to compute BSD invariants: {e}")

    print("-" * 40)

# Loop over each curve
for i, coeffs in enumerate(curves, 1):
    print(f"Curve {i}: y^2 = x^3 + {coeffs[3]}x + {coeffs[4]}")
    elliptic_curve_analysis(coeffs)