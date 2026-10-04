try:
    from src.physics.geodesics import GeodesicIntegrator
    GI = GeodesicIntegrator()
    geos = [GI.integrate(X[i], steps=200) for i in range(5)]
except:
    geos = [np.cumsum(np.random.normal(scale=0.01, size=(200,3)), axis=0) for _ in range(5)]
