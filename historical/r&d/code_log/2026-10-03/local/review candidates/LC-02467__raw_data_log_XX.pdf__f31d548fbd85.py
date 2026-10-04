results = []

for name, r, rho in clusters:
    P_pred = predict_generator(r, rho)
    a, b = derive_curve(r, rho)

    rank = "Error"
    P_actual = None
    try:
        E = EllipticCurve(QQ, [a, b])
        # Force 2-descent
        E.two_descent(second_limit=15, verbose=False)
        rank = E.rank(only_use_mwrank=False)
        gens = E.gens()
        P_actual = normalize_point(gens[0]) if rank > 0 else None
    except Exception as e:
        print(f"{name}: {e}")

    match = (P_actual is not None and P_pred == P_actual)

    results.append({
        "Cluster": name,
        "r": r,
        "ρ": rho,
        "a": a,
        "b": b,
        "Rank": rank,
        "Predicted P": str(P_pred),
        "Actual P": str(P_actual) if P_actual else "—",