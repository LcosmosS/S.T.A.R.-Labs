# Basic summaries
rec_df["log_abs_delta"] = np.log10(rec_df["delta"].abs().replace(0, np.nan)).replace(-np.inf, np.nan)
rank_counts = rec_df["rank"].value_counts().sort_index()
mean_log_delta = rec_df.groupby("rank")["log_abs_delta"].mean().round(4)

print("Rank distribution:\n", rank_counts)
print("\nMean log10|Δ| by rank:\n", mean_log_delta)
