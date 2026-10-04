results = []
for name, r, rho in clusters:
    P_pred = predict_star_generator(r, rho)
    a = -round(31.59259 * r)
    b = rho
    try:
        E = EllipticCurve(QQ, [a, b])
        E.two_descent(second_limit=15, verbose=False)
        rank = E.rank(only_use_mwrank=False)
        gens = E.gens()
        P_actual = gens[0] if rank > 0 else None
    except:
        rank = "Error"
        P_actual = None
    match = (P_actual is not None and P_pred == P_actual)
    results.append({
        "Cluster": name, "r": r, "ρ": rho,
        "Predicted P": str(P_pred), "Rank": rank,
        "Actual P": str(P_actual) if P_actual else "—", "Match": "YES" if match else "NO"
    })


df = pd.DataFrame(results)
print(df.to_string(index=False))
