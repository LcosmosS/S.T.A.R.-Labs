           from  src.physics.entropy_field        import   EntropyField
           EF  = EntropyField()
           entropy   =  np.array([EF.M(p)     for  p  in  X])
           curvature    = np.array([EF.curvature(p)        for  p  in X])
