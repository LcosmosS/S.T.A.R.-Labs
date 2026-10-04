           from  src.physics.metric_perturbations          import  MetricPerturbations
           MP  = MetricPerturbations()

           delta_g_list    =  [MP.delta_g(p)     for  p in  points]
           scalar_modes    =  np.array([MP.scalar_modes(p)        for  p  in points])     # (phi, psi)
