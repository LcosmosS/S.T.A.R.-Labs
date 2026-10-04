                    alpha=0.3,
                    linewidth=0.5
                )
        # Label high-rank curves
        if interweb_data[i][2] >= 2:
            ax.text(log_deltas[i], log_conds[i], ranks[i], f'({interweb_data[i][0]},{interweb_data[i][1]})', size=8)

    ax.set_xlabel('Log(Discriminant)')
    ax.set_ylabel('Log(Conductor)')
    ax.set_zlabel('Rank (Nodes in Cosmic Web)')
    ax.set_title('Cosmic Interweb: Nodes and Filaments')
    plt.savefig("interweb_plot.png")
    plt.close()

print(f"\nCompleted: {successful_curves} successful curves analyzed out of {attempts} attempts")
if X_data:
    print("\nFinal classifier data summary:")
    print(f"Total curves analyzed: {len(X_data)}")
    print(f"Success rate: {sum(y_data) / len(y_data):.2%}")
if interweb_data:
    print("\nInterweb nodes saved to interweb_nodes.txt")