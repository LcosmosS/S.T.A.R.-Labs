# SageMath Script Log 1: Non-Singularity and Discriminant Verification
# Define the elliptic curve over Rational Field Q
E = EllipticCurve(QQ, [-1706, 6320])

a = E.a4()
b = E.a6()
delta = E.discriminant()

print(f"Defined Curve: y^2 = x^3 + ({a})*x + ({b})")
print(f"Calculated Discriminant Delta: {delta}")
print(f"Prime Factorization of Delta: {factor(delta)}")
