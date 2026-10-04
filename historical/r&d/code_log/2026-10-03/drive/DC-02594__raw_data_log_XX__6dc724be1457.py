def recursive_denoms(n, base=3):
1.     return base ** (2*n + 2)
   * n=1 → 34=81 3^{4} = 81 34=81 (matches x-denominator)
   * n=2 → 36=729 3^{6} = 729 36=729 (matches y-denominator)
   * n=3 → 38=6561 3^{8} = 6561 38=6561 (next predicted term)
