results = []


for name, r, rho in clusters:
    # Predict
    P_pred = predict_star_generator(r, rho)
    
    # Derive curve
    kappa = 31.59259259259259
    a = -round(kappa * r)
    b = rho
    
    # Compute actual
    rank_actual = "Error"
    P_actual = None
    try:
        E = EllipticCurve(QQ, [a, b])
        E.two_descent(second_limit=20, verbose=False)
        rank_actual = E.rank(only_use_mwrank=False)
        gens = E.gens()
        P_actual = normalize_point(gens[0]) if rank_actual > 0 else None
    except Exception as e:
        print(f"{name}: {e}")
    
    # Match
    match = (P_actual is not None and P_pred == P_actual)
    
    results.append({
        "Cluster": name,
        "r": r,
        "ρ": rho,
        "a": a,
        "b": b,
        "Rank": rank_actual,
        "Predicted P": str(P_pred),
        "Actual P": str(P_actual) if P_actual else "—",
        "Match": "YES" if match else "NO"
    })


# ———————— RESULTS ————————
df = pd.DataFrame(results)
print("\n" + df.to_string(index=False))
