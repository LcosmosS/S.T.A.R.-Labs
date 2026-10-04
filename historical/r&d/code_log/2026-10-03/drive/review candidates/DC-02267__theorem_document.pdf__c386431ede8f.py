# Example: Computing rank and L-function for E: y^2 = x^3 - x
from sage.all import EllipticCurve
E = EllipticCurve([0, -1])
rank = E.rank()
L = E.lseries()
L1 = L(1) # Value at s=1
print('Rank:', rank)
print('L(1):', L1)
