    sizes = [float(max(x[3] * 100, 1e-6)) for x in interweb_data]
    scatter = ax.scatter(log_deltas, log_conds, ranks, s=sizes, c=volumes, cmap='magma',
alpha=0.7)
    plt.colorbar(scatter, label='Comoving Volume (Mly^3)')
    for i, (a, b, rank, _, _, reg, _, _, log_delta, log_cond, _) in enumerate(interweb_data):
        for j in range(i + 1, len(interweb_data)):
            reg_diff = abs(interweb_data[i][5] - interweb_data[j][5])
            if reg_diff < 10000:
                weight = 1 / (1 + reg_diff / 100)
                if weight > 0.5:
                    ax.plot([log_deltas[i], log_deltas[j]], [log_conds[i], log_conds[j]], [ranks[i], ranks[j]],
'b-', alpha=0.5 * weight, linewidth=0.7 * weight)
        if rank >= 2:
            color = 'red' if rank == 3 else 'blue'
            offset = 0.5 if log_delta > 20 else -0.5
            ax.text(log_delta + offset, log_cond + offset, rank + 0.1, f'({a},{b})', size=8, color=color)
    ax.set_xlabel('Log(|Discriminant|)')
    ax.set_ylabel('Log(|Conductor|)')
    ax.set_zlabel('Rank')
    ax.set_title('Cosmic Interweb: Nodes and Weighted Filaments (Improved)')
    ax.grid(True)
    plt.savefig("interweb_improved_with_twist2.png")
    plt.close()
    print("Improved cosmic interweb plot saved as interweb_improved_with_twist2.png")
except Exception as e:
    print(f"Failed to generate improved interweb plot: {e}")

print(f"\nFinal training data: {training_data}")
print(f"Final labels: {training_labels}")
