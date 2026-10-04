def quadratic_twist(E, d):
a, b = E.a4(), E.a6()
return EllipticCurve(QQ, [0, 0, 0, d2 * a, d3 * b])
