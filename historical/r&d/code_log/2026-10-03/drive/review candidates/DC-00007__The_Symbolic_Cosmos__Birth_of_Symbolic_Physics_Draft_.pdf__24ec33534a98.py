# We will use SageMath to compute the real period.
E = EllipticCurve(QQ, [-1706, 6320])
print(E.period_lattice().real_period())
