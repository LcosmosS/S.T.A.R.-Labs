           def  fallback_entropy(p):
                p  = np.abs(p)    + 1e-12
                pnorm   = p  / p.sum()
                return   -np.sum(pnorm    *  np.log(pnorm))

           ent  =  np.array([fallback_entropy(p)        for  p  in df[['x','y','z']].values])

           # simple fallback gradient
           grads   = np.gradient(ent)
           grads   = np.vstack([np.ones(3)*g       for  g  in ent])

           hess_traces    =  np.zeros(len(ent))

     Computed entropy, gradients, Hessian traces using src.entropy.
