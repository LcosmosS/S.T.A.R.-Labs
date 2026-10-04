E = EllipticCurve([-1706, 6320])
L = E.lseries()
L_value = L.dokchitser(prec=100).derivative(1, 1)
Omega = E.period_lattice().real_period(prec=100)
print(L_value, Omega)


* L'(E, 1) \approx 5.7161472701821916623395660050: This is the first derivative of the L-function at s = 1, confirming the analytic rank is 1 (since L(E, 1) = 0, and this derivative is non-zero).
* \Omega \approx 0.42236269178325809849360427108: This is the real period of the curve, computed with higher precision.
