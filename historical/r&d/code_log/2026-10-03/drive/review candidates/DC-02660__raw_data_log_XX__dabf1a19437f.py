results = []
for name, r, rho in clusters:
    # Predict
    P_pred = predict_generator(r, rho)
    a, b = derive_curve(r, rho)
   
    # Compute actual curve
    try:
        E = EllipticCurve(QQ, [a, b])
        rank = E.rank()
        gens = E.gens()
        P_actual = gens[0] if rank > 0 else None
    except:
        rank = "Error"
        P_actual = None
   
    # Match
    match = (P_actual is not None and P_pred == P_actual)
   
    results.append({
        "Cluster": name,
        "r": r,
        "ρ": rho,
        "a": a,
        "b": b,
        "Predicted P": str(P_pred),
        "Actual Rank": rank,
        "Actual P": str(P_actual) if P_actual else "—",
        "Match": "YES" if match else "NO"
    })
# ———————— SUMMARY TABLE ————————
df = pd.DataFrame(results)
print(df.to_string(index=False))
