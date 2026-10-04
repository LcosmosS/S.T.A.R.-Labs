      ax  = fig.add_subplot(111, projection='3d')

      sc  = ax.scatter(
           df['x'], df['y'], df['z'],
           c=df.get('rank',     0),
           s=20  +  30*df.get('regulator',       0),
           cmap='viridis', alpha=0.8
      )

      ax.set_xlabel('Rank')
      ax.set_ylabel('log10(Conductor)')
      ax.set_zlabel('Regulator')
      plt.title('ACSC Projection Φ(E)')
      plt.colorbar(sc, label='Rank')
      plt.tight_layout()
      plt.savefig('results/projection_scatter.png', dpi=200)
      plt.show()

      print("Saved results/projection_scatter.png")






























                                                        4
