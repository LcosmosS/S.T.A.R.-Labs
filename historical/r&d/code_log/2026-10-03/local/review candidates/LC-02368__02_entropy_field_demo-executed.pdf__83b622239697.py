           from  src.entropy.entropy_field        import   EntropyField
           from  src.entropy.entropy_shells        import   EntropyShells

           M  = EntropyField()
           S  = EntropyShells(M)

           points   = df[['x','y','z']].values
           ent  =  np.array([M.entropy(p)      for  p  in  points])
           grads   = np.vstack([M.gradient(p)       for  p  in  points])
           hess_traces    =  np.array([np.trace(M.hessian(p))         for  p in  points])

           print("Computed entropy, gradients, Hessian traces using src.entropy.")

      except   Exception   as  e:
           print("src.entropy not available; using local fallback computations.", e)



                                                        2