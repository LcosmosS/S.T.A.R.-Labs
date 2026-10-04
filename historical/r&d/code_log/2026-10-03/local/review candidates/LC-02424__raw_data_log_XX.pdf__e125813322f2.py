def coma_sequence(n, seed=321):
    if n == 0:
        return seed

    2.      return coma_sequence(n-1) + (9980 // (n+1))
             ○   Term 0: 321
