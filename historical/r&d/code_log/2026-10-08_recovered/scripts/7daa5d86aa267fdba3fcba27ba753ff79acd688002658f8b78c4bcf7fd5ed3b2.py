from sage.all import Integer, kronecker
N = Integer(98713152)
D = -3
prime_factors = N.prime_factors()
for p in prime_factors:
    k = kronecker(D, p)
    print(f"p={p}, k={k}")
    if k == 0 and p**2.divides(N) and (-D) % p == 0:
        print("Condition passed")