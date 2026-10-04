                if weight > 0.5:
                    ax.plot([log_deltas[i], log_deltas[j]], [log_conds[i], log_conds[j]], [ranks[i], ranks[j]],
'b-', alpha=0.5 * weight, linewidth=0.7 * weight)
        if rank >= 2:
            color = 'red' if rank == 3 else 'blue'
            # Add a small offset to avoid overlaps
            offset = 0.5 if log_delta > 20 else -0.5  # Adjust based on position
            ax.text(log_delta + offset, log_cond + offset, rank + 0.1, f'({a},{b})', size=8, color=color)
    ax.set_xlabel('Log(Discriminant)')
    ax.set_ylabel('Log(Conductor)')
    ax.set_zlabel('Rank')
    ax.set_title('Cosmic Interweb: Nodes and Weighted Filaments (Improved)')
    ax.grid(True)
    plt.savefig("interweb_improved_with_twist.png")
    plt.close()
    print("Improved cosmic interweb plot saved as interweb_improved_with_twist.png")
except Exception as e:
    print(f"Failed to generate improved interweb plot: {e}")

print(f"\nFinal training data: {training_data}")
print(f"Final labels: {training_labels}")
