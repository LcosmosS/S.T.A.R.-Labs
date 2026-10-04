fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")

ax.scatter(points[:, 0], points[:, 1], points[:, 2], c="lightgray", s=8, alpha=0.6)

colors = ["C0", "C1", "C2", "C3", "C4"]
for i, traj in enumerate(trajectories):
    ax.plot(
        traj[:, 0], traj[:, 1], traj[:, 2], color=colors[i], lw=2, label=f"geodesic_{i}"
    )

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
plt.title("Entropy Geodesics on Symbolic Manifold")
plt.legend()

plt.savefig("results/geodesics_overlay.png", dpi=200)
plt.show()

print("Saved results/geodesics_overlay.png and results/geodesics.npy")