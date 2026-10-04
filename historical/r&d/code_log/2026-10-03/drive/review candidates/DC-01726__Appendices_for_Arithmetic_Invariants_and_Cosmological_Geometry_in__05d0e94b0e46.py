    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(df_proj['ra_norm'], df_proj['dec_norm'],
                         df_proj['comoving_norm'], c=df_proj['rank'], cmap='viridis')
    ax.set_xlabel('RA (norm, +/-)')
    ax.set_ylabel('DEC (norm, +/-)')
    ax.set_zlabel('Comoving (norm, +/-)')
    ax.set_title('HD 3D Manifold (Binned by Generator Type)')
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
            formula = f"rank = bit_length(abs(int(Δ))) // 3 + 1 = {bit_len} // 3 + 1 = {rank_class}"
            calculation = f"Δ = -16 * (4*{a}^3 + 27*{b}^2) = {disc}\nBit length = {bit_len}"
            analysis = f"Class {rank_class}: This rank approximates Mordell-Weil r(E) via Δ complexity (log2 scale proxy), inspired by Selmer bounds in descent theory (e.g., 3-Selmer impasse resolution). For recursive gens (i={i}), rank grows ~ log2(O(PHI**(3*i))) due to exponential Δ, tying to GLMPCT paradox correction and ACSC bijection (r(E) ~ cosmic rank_cosmo(G)). In Cosmic BSD, higher rank correlates with curvature ∫ Ricci dV in dense cosmic regions. Per ECC, this stratifies entropy field ℳ(x) into shells ℳ_n with golden-ratio recurrence."
            output = f"\nRank Class {rank_class}:\nEquation: {equation}\nFormula: {formula}\nCalculation: {calculation}\nAnalysis: {analysis}\n"
            print(output)
            logger.info(output)
            with open('ucf_analysis.txt', 'a') as f:
                f.write(output)


# Main Test
if __name__ == '__main__':
    start_time = time.time()
    logger.info("Starting UCF Test v5")


    # Load and impute large CSV
    df_cosmo = load_and_impute_large_csv(INPUT_FILE)
    logger.info(f"Loaded and imputed {len(df_cosmo)} rows.")


    # Generate curves
    df_curves = generate_elliptic_curves(SAMPLE_CURVES)
    logger.info(f"Generated {len(df_curves)} curves with deciphered ranks.")


    # Print rank classes
    print_rank_classes(df_curves)


    # Bin by generator
    bin_by_generator(df_curves)


    # Compute projection
    df_proj = compute_projection(df_curves)


    # Align with cosmic data
    df_aligned = align_projections(df_cosmo, df_proj)


    # Visualize HD 3D manifold MP4
    visualize_hd_manifold(df_aligned, duration=45)


    logger.info(f"Test complete. Time: {time.time() - start_time:.2f}s")
    with open('ucf_analysis.txt', 'a') as f:
        f.write(f"Test complete. Time: {time.time() - start_time:.2f}s\n")
