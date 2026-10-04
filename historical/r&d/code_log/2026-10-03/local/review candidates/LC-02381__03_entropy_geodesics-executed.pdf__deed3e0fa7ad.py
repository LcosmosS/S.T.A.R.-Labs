       endpoints    =  np.array([traj[-1]        for  traj   in  trajectories])

       dists   = np.linalg.norm(endpoints[:,None,:]              -  endpoints[None,:,:], axis=2)
       avg_divergence      =  np.mean(dists[np.triu_indices(len(dists), k=1)])

       print("Average geodesic endpoint divergence:", avg_divergence)

      Average geodesic endpoint divergence: 2.0318723710096473
      Interpretation.
