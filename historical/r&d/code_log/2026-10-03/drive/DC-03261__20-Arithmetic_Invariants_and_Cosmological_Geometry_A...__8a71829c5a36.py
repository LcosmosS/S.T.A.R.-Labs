def visualize_hd_manifold(df_proj, duration=45): scaler = StandardScaler() df_proj[['ra_norm', 'dec_norm', 'comoving_norm']] = scaler.fit_transform(df_proj[['ra', 'dec', 'comoving']])
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(df_proj['ra_norm'], df_proj['dec_norm'], df_proj['comoving_norm'], c=df_proj['rank'], cmap='viridis')
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
