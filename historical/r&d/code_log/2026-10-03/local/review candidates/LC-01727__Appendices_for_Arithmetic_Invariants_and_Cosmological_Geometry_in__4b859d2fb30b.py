    cbar = plt.colorbar(scatter)
    cbar.set_label('Rank')
    plt.savefig(f'{PLOT_PREFIX}_manifold.png')
    logger.info("Static manifold PNG saved.")

    frames = int(duration * 2)  # ~2 fps

    def animate(frame):
        ax.view_init(elev=30, azim=frame * (360 / frames))
        return scatter,

    ani = FuncAnimation(fig, animate, frames=frames, interval=500)
    ani.save(f'{PLOT_PREFIX}_animation.mp4', writer='ffmpeg', dpi=100)
    logger.info(f"MP4 animation saved ({duration}s).")

# Print human-readable for each unique rank class
def print_rank_classes(df_curves):
    df_curves['rank_class'] = df_curves['rank'].astype(
        int)  # Group by integer rank
    unique_ranks = sorted(df_curves['rank_class'].unique())
    for rank_class in unique_ranks:
        group = df_curves[df_curves['rank_class'] == rank_class]
        if not group.empty:
            rep = group.iloc[0]  # Representative curve
            i, a, b, disc = rep['i'], rep['a'], rep['b'], rep['discriminant']
            disc_int = int(abs(disc))
            bit_len = disc_int.bit_length() if disc_int > 0 else 0
            equation = f"y^2 = x^3 + {a}*x + {b}"
            formula = f"rank = bit_length(abs(int(Δ))) // 3 + 1 = {bit_len} // 3 + 1 =
