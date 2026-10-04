try:
    from src.physics.metric_perturbations import MetricPerturbations

    MP = MetricPerturbations()

    delta_g_list = [MP.delta_g(p) for p in points]
    scalar_modes = np.array([MP.scalar_modes(p) for p in points])  # (phi, psi)
    traces = np.array([np.trace(dg) for dg in delta_g_list])

    print("Computed delta_g and scalar modes using src.physics.metric_perturbations")

except Exception as e:
    print("MetricPerturbations not available; using fallback approximations.", e)

    delta_g_list = [np.eye(3) * np.sum(p) for p in points]
    scalar_modes = np.vstack([[np.sum(p), -np.sum(p)] for p in points])
    traces = np.array([np.trace(dg) for dg in delta_g_list])