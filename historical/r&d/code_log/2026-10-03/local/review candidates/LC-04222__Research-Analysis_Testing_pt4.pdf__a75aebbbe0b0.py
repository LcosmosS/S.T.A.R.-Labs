                    alpha=0.5 * weight,
                    linewidth=0.7 * weight
                )
        if filtered_data[i][2] >= 2:
            color = 'red' if filtered_data[i][2] == 3 else 'blue'
            ax.text(log_deltas[i], log_conds[i], ranks[i],
                    f'({filtered_data[i][0]},{filtered_data[i][1]}): 54.0 Mly',
                    size=8, color=color)

    ax.set_xlabel('Log(Discriminant)')
    ax.set_ylabel('Log(Conductor)')
    ax.set_zlabel('Rank')
    ax.set_title('Cosmic Interweb: Nodes and Weighted Filaments')
    plt.savefig("interweb_plot.png")
    plt.close()

print(f"\nCompleted: {successful_curves} successful curves analyzed out of {attempts} attempts")
