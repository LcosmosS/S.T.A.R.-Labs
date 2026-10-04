# Histogram
plt.figure(figsize=(6, 4))
plt.hist(df["entropy"], bins=30, color="C0", alpha=0.8)
plt.title("Entropy Histogram")
plt.xlabel("M(x)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("results/entropy_hist.png")
plt.show()

# 2D quiver on x-y plane
plt.figure(figsize=(6, 6))
sample = df.sample(min(200, len(df)))
X = sample["x"].values
Y = sample["y"].values
U = grads[: len(sample), 0]
V = grads[: len(sample), 1]

plt.quiver(X, Y, U, V, scale=10, width=0.003)
plt.scatter(X, Y, c=sample["entropy"], cmap="plasma", s=20)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Entropy gradient (quiver)")
plt.savefig("results/entropy_quiver.png")
plt.show()

# Hessian trace scatter
plt.figure(figsize=(6, 4))
plt.scatter(df["entropy"], df["hess_trace"], s=10, alpha=0.7)
plt.xlabel("Entropy")
plt.ylabel("Trace(Hessian)")
plt.title("Hessian trace vs Entropy")
plt.savefig("results/hess_trace_vs_entropy.png")
plt.show()