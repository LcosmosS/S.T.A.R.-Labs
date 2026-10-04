try:
    from src.physics.metric_perturbations import MetricPerturbations
    MP = MetricPerturbations()
    delta_g = [MP.delta_g(p) for p in X]
    scalar_modes = np.array([MP.scalar_modes(p) for p in X])
except:
    delta_g = [np.eye(3)*np.sum(p) for p in X]
    scalar_modes = np.vstack([[np.sum(p), -np.sum(p)] for p in X])
