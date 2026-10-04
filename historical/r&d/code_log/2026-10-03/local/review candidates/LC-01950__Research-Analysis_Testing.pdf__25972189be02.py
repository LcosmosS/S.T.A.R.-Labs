E = EllipticCurve([-1706, 6320])
Omega = E.period_lattice().real_period()
Tamagawa = prod(E.tamagawa_numbers())
print(Omega, Tamagawa)


    ●   0.422362691783258: This is \Omega, the real period of the curve.
