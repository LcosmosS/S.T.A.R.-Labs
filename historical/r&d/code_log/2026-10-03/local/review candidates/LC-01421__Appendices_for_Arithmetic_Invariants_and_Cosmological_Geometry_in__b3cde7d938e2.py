    try:
        E = EllipticCurve(QQ, [0, 0, 0, float(a), float(b)])

        delta = E.discriminant()
        conductor = E.conductor()
        tors_order = E.torsion_subgroup().order()

        print(f"Discriminant : {delta}")
        print(f"Conductor    : {conductor}")
        print(f"Torsion order: {tors_order}")

        # --- Rank & BSD Verification ---
        rank = E.rank()
        selmer_rank = E.selmer_rank()
        estimated_3selmer = max(rank, selmer_rank - 1)

        print(f"Algebraic rank      : {rank}")
        print(f"2-Selmer rank       : {selmer_rank}")
        print(f"Estimated 3-Selmer  : {estimated_3selmer}")

        # Analytic rank via L-series
        L = E.lseries()
        dok = L.dokchitser(prec=100)
        L1 = dok(1)

        analytic_rank = 0
        leading_coeff = float(L1)
