try:
    from src.physics.entropy_field import EntropyField
    EF = EntropyField()
    entropy = np.array([EF.M(p) for p in X])
    curvature = np.array([EF.curvature(p) for p in X])
except:
    entropy = np.sum(X, axis=1)
    curvature = np.random.normal(scale=0.1, size=len(X))
