           from  src.entropy.entropy_geodesics         import   EntropyGeodesics
           G  = EntropyGeodesics()

           trajectories    =  []
           for  i  in range(5):
                idx  =  np.random.randint(0,      len(points))
                x0  = points[idx]
                v0  = np.random.normal(scale=0.1, size=3)
                traj  =  G.geodesic(x0, v0, steps=80)
                trajectories.append(traj)

           trajectories    =  np.array(trajectories)
           np.save('results/geodesics.npy', trajectories)

           print("Computed geodesics using src.entropy.entropy_geodesics")

      except   Exception   as  e:
           print("EntropyGeodesics not available; using simple straight-line fallback.

        ↪", e)



                                                        2
