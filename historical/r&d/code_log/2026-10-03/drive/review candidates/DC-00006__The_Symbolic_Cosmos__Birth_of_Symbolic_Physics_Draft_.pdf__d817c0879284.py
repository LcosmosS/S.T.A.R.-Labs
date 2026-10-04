# We will use SageMath to compute the regulator.
E = EllipticCurve(QQ, [-1706, 6320])
print(E.regulator())
