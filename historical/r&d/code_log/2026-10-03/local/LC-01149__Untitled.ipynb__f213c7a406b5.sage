# SageMath Script Log 3: L-Series Derivatives and Real Period at 100-bit Precision
E = EllipticCurve(QQ, [-1706, 6320])
L = E.lseries()

# Evaluate L(E, s) and its first derivative at s=1 with 100-bit precision
L_val = L.dokchitser(prec=100).derivative(1, 0)
L_prime = L.dokchitser(prec=100).derivative(1, 1)
omega = E.period_lattice().real_period(prec=100)

print(f"L(E, 1) Value: {L_val}")
print(f"L'(E, 1) Derivative Value: {L_prime}")
print(f"Real Period Omega Value: {omega}")