# Define the elliptic curve
E = EllipticCurve(QQ, [-1706, 6320]) # y^2 = x^3 - 1706x + 6320 over QQ
# Define the point P = (2, 54)
P = E([2, 54])
# Compute the canonical height with 100 bits of precision
Reg = P.height(precision=100) # Note: 'prec' is often 'precision' in SageMath
# Print the regulator
print(Reg)
