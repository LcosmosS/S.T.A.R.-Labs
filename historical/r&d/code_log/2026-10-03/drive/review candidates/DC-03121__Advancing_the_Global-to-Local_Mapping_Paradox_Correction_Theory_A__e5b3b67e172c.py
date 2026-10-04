# Cosmological mapping section
try:
    cosmological_coords = []
    for a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, log_delta, log_cond, volume in interweb_data:
        if volume <= 0 or omega is None or reg is None:
            continue
        # Map to 3D cosmological coordinates
        # Use log_delta, log_cond, and volume to determine position
        x_cosmo = log_delta * 1e6  # Scale to megaparsecs
        y_cosmo = log_cond * 1e6
        z_cosmo = volume * 1e12  # Scale volume for visibility
        cosmological_coords.append((x_cosmo, y_cosmo, z_cosmo, rank, volume))


    if cosmological_coords:
        fig = plt.figure(figsize=(14, 12))
        ax = fig.add_subplot(111, projection='3d')
        x_coords = [x for x, y, z, r, v in cosmological_coords]
        y_coords = [y for x, y, z, r, v in cosmological_coords]
        z_coords = [z for x, y, z, r, v in cosmological_coords]
        ranks = [r for x, y, z, r, v in cosmological_coords]
        volumes = [v for x, y, z, r, v in cosmological_coords]
        sizes = [max(v * 100, 1e-6) for v in volumes]
        colors = ['k' if r == 0 else 'g' if r == 1 else 'b' if r == 2 else 'r' for r in ranks]
        
        scatter = ax.scatter(x_coords, y_coords, z_coords, s=sizes, c=colors, alpha=0.7)
        ax.scatter([virgo_log_delta * 1e6], [virgo_log_cond * 1e6], [VIRGO_COMOVING_VOLUME * 1e12], s=200, c='green', marker='*', label='Virgo Supercluster')
        
        ax.set_xlabel('X (Mpc)')
        ax.set_ylabel('Y (Mpc)')
        ax.set_zlabel('Z (Scaled Volume)')
        ax.set_title('Cosmological Mapping: Nodes and Virgo Supercluster')
        ax.grid(True)
        ax.legend()
        plt.savefig("cosmological_mapping_v2.png")
        plt.close()
        log_print("Cosmological mapping plot saved as cosmological_mapping_v2.png")
    else:
        log_print("No valid cosmological coordinates available; skipping cosmological mapping plot")
except Exception as e:
    log_print(f"Failed to generate cosmological mapping plot: {e}")
