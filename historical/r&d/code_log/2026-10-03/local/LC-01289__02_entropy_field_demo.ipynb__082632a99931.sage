thresholds = np.quantile(df["entropy"], [0.0, 0.33, 0.66, 1.0])

try:
    shells = [S.assign_shell(p, thresholds) for p in df[["x", "y", "z"]].values]
    df["shell"] = shells
except Exception:
    df["shell"] = pd.cut(
        df["entropy"], bins=thresholds, labels=False, include_lowest=True
    )

df.to_csv("results/entropy_summary.csv", index=False)
print("Assigned shells and updated results/entropy_summary.csv")