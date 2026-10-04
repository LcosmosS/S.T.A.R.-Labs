import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid", context="notebook")

# Boxplot: log|Δ| by rank
plt.figure(figsize=(8,4))
sns.boxplot(x="rank", y="log_abs_delta", data=rec_df)
plt.title("log10|Δ| by algebraic rank")
plt.savefig(os.path.join(OUT_DIR, "box_logdelta_by_rank.png"), dpi=150)
plt.show()

# Scatter: aligned coords (first 5000 points) colored by rank (for visual sanity)
sample = rec_df.sample(min(5000, len(rec_df)), random_state=SEED)
plt.figure(figsize=(6,6))
plt.scatter(sample["x_aligned"], sample["y_aligned"], c=sample["rank"], cmap="viridis", s=6, alpha=0.6)
plt.colorbar(label="rank")
plt.title("Aligned primary projection (x vs y) colored by rank (sample)")
plt.savefig(os.path.join(OUT_DIR, "aligned_xy_sample.png"), dpi=150)
plt.show()
