      try:
           from  src.projection.projection        import   project_invariants
           print("Using src.projection.project_invariants")
           points   = np.vstack(df.apply(lambda        r: project_invariants(r), axis=1).

        ↪to_list())
      except   Exception:
           print("Using local fallback projection.")
           def  fallback_project(row):
                return   np.array([
                     row.get('rank',     0),
                     np.log10(row.get('conductor',         1) +  1e-12),
                     row.get('regulator',      0)
                ])
           points   = np.vstack(df.apply(fallback_project, axis=1).to_list())

      df['x'], df['y'], df['z']        = points[:,0], points[:,1], points[:,2]
      df.to_csv('results/projection_points.csv', index=False)


                                                        3