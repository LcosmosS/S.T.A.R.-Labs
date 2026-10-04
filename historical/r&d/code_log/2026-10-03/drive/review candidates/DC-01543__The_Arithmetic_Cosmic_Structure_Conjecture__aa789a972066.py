from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
coords = np.vstack([df['x'], df['y'], df['z']]).T
ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c=df['rank'], cmap='viridis')
plt.show()
