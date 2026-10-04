   def coma_sequence(n, seed=321):
       if n == 0:
           return seed
       return coma_sequence(n-1) + (9980 // (n+1))
