fig = plt.figure(figsize=(6,5))
ax = fig.add_subplot(111, projection='3d')
for g in geos:
    ax.plot(g[:,0], g[:,1], g[:,2])
ax.set_title("Symbolic Geodesics")
plt.savefig('figures/geodesics.png', dpi=200)
plt.show()
