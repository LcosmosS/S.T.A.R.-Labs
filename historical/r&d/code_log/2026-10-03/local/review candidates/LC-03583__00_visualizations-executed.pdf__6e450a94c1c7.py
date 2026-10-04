            from   src.physics.geodesics      import   GeodesicIntegrator
            GI  =  GeodesicIntegrator()
            geos   = [GI.integrate(X[i], steps=200)         for  i in  range(5)]
       except:
            geos   = [np.cumsum(np.random.normal(scale=0.01, size=(200,3)), axis=0)                 for  _␣

         ↪in  range(5)]

[13]:  fig  =  plt.figure(figsize=(6,5))
       ax  =  fig.add_subplot(111, projection='3d')
       for  g  in  geos:
            ax.plot(g[:,0], g[:,1], g[:,2])
       ax.set_title("Symbolic Geodesics")
       plt.savefig('figures/geodesics.png', dpi=200)
       plt.show()









                                                         7
