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
