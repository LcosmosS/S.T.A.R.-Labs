pari.default('realprecision', 60)

def triangulate_curve(a4, a6):
    E_sage = EllipticCurve([a4, a6])
    E_pari = pari.ellinit([a4, a6])

    print("\n=== Curve Data ===")
    print("Weierstrass model:", E_sage)

    # Sage rank bounds
    try:
        sage_lower, sage_upper = E_sage.rank_bounds()
    except Exception as e:
        print("Sage rank_bounds failed:", e)
        sage_lower, sage_upper = None, None

    print("Sage rank lower bound:", sage_lower)
    print("Sage rank upper bound:", sage_upper)

    # PARI 2-descent / 2-Selmer via ellrank
    try:
        pari_rank_data = E_pari.ellrank()
        pari_mordell = pari_rank_data[0]
        pari_selmer_upper = pari_rank_data[1]
    except Exception as e:
        print("PARI ellrank failed:", e)
        pari_mordell, pari_selmer_upper = None, None

    print("PARI Mordell rank (ellrank[0]):", pari_mordell)
    print("PARI 2-Selmer upper bound (ellrank[1]):", pari_selmer_upper)

    # PARI analytic rank
    try:
        ar = E_pari.ellanalyticrank()
        analytic_rank = ar[0]
        Lprime = ar[1]
    except Exception as e:
        print("PARI analytic rank failed:", e)
        analytic_rank, Lprime = None, None

    print("Analytic rank:", analytic_rank)
    print("L'(E,1):", Lprime)

    # Triangulation
    print("\n=== Triangulated Consensus ===")

    if None in (sage_lower, sage_upper, pari_selmer_upper, analytic_rank):
        print("Insufficient data for consensus.")
        return

    lower = max(analytic_rank, sage_lower)
    upper = min(sage_upper, pari_selmer_upper)

    print(f"Lower bound (max(analytic, Sage lower)): {lower}")
    print(f"Upper bound (min(Sage upper, PARI Selmer)): {upper}")

    if lower == upper:
        print("Consensus: Rank is exactly", lower)
    else:
        print(f"No consensus: rank in [{lower}, {upper}]")

# Rank Triangulation
triangulate_curve(-1706, 6320)


