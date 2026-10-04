# robust_rank_test.py
from sage.all import *

def safe_rank(E, limit=20):
    try:
        E.two_descent(second_limit=limit, verbose=False)
        return E.rank(only_use_mwrank=False)
    except:
        return "Failed"

clusters = [...]  # same as before

for name, r, rho in clusters:
    a = -round(31.59259 * r)
    b = rho
    E = EllipticCurve(QQ, [a, b])
    rank = safe_rank(E)
    print(f"{name}: rank = {rank}")
