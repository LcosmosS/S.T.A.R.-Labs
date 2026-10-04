    print(f"\nProcessing cluster: {cluster_name}")
    try:
        # Predict coefficients using the Virgo-calibrated kappa
        a_predicted = -VIRGO_CALIBRATED_KAPPA * r
        b_predicted = rho

        # Round 'a' as is standard for number-theoretic investigations
        a = round(a_predicted)
        b = b_predicted

        print(f"  Derived curve: y^2 = x^3 + {a}x + {b}")

        # Define the curve in SageMath
        E = EllipticCurve(QQ, [a, b])

        # Compute algebraic rank and generator
        rank = E.rank()

        if rank == 1:
            generator = E.gens()[0]
            print(f"  SUCCESS: Rank 1 curve found.")
            print(f"  Generator: {generator}")
            return {
                'cluster': cluster_name, 'r': r, 'rho': rho,