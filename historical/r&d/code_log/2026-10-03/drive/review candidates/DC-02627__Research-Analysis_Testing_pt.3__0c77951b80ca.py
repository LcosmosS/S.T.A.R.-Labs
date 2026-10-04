    scatter = ax.scatter(log_deltas, log_conds, ranks, s=sizes, c=colors, cmap='viridis')
    plt.colorbar(scatter, label='Weak BSD Holds')
    ax.set_xlabel('Log(Discriminant)')
    ax.set_ylabel('Log(Conductor)')
    ax.set_zlabel('Rank')
    plt.savefig("interweb_plot.png")
    plt.close()


print(f"\nCompleted: {successful_curves} successful curves analyzed out of {attempts} attempts")
if X_data:
    print("\nFinal classifier data summary:")
    print(f"Total curves analyzed: {len(X_data)}")
    print(f"Success rate: {sum(y_data) / len(y_data):.2%}")
if interweb_data:
    print("\nInterweb nodes saved to interweb_nodes.txt")
    print("Sample nodes:", interweb_data[:2])
    print("Interweb plot saved to interweb_plot.png")
