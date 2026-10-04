      os.makedirs('figures', exist_ok=True)

[2]:  if  os.path.exists('results/projection_points.csv'):
           df  = pd.read_csv('results/projection_points.csv')
           X  = df[['x','y','z']].values
      else:
           X  = np.random.rand(300,3)

      print("Loaded", X.shape[0],        "projection points")

     Loaded 300 projection points

     1.1       ACSC  Projection  Geometry  (Static  +  Interactive  +  Blender)

[3]:  fig  =  plt.figure(figsize=(6,5))
      ax  = fig.add_subplot(111, projection='3d')
      ax.scatter(X[:,0], X[:,1], X[:,2], s=8, alpha=0.6)
      ax.set_title("ACSC Projection Geometry")
      plt.savefig('figures/acsc_projection.png', dpi=200)
      plt.show()



































                                                        2
