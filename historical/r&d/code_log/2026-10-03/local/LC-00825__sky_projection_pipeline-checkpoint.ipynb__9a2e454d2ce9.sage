# 5. Advanced 3D Visualization
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Arithmetic Projection
scatter_arith = ax.scatter(embedded[:, 0], embedded[:, 1], embedded[:, 2],
                           c=arithmetic_data['rank'], cmap='viridis',
                           s=6, alpha=0.6, label='Arithmetic Projection')

# Real Galaxies Overlay
if len(galaxies) > 0:
    gal_subset = galaxies.sample(min(1500, len(galaxies)))
    ax.scatter(gal_subset['ra']/12, gal_subset['dec']/6, gal_subset['z']*8,
               c='red', s=2, alpha=0.3, label='Real Galaxies')

ax.set_xlabel('Cosmic X')
ax.set_ylabel('Cosmic Y')
ax.set_zlabel('Cosmic Z')
ax.set_title('S.T.A.R. Arithmetic → Cosmic Projection\nwith Real Galaxy Overlay')
plt.legend()
plt.show()