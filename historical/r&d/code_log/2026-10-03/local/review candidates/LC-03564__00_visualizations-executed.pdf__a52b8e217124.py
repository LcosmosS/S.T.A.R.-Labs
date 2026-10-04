            from   src.physics.metric_perturbations         import   MetricPerturbations
            MP  =  MetricPerturbations()
            delta_g   =  [MP.delta_g(p)     for  p in  X]
            scalar_modes     = np.array([MP.scalar_modes(p)        for  p  in  X])
