# High-precision verification for E: y^2 = x^3 - 1706*x + 6320

E = EllipticCurve(QQ, [-1706, 6320])

print("=== Basic invariants ===")
print("Discriminant     =", E.discriminant().factor())
print("Conductor        =", E.conductor())
print("Tamagawa product =", E.tamagawa_product())
print("Torsion          =", E.torsion_order())
print("Generators       =", E.gens())
print()

# Set high precision (200 bits ≈ 60 decimal digits)
prec = 200
Eprec = E.change_ring(ComplexField(prec))   # for analytic computations

print("=== Real period Ω ===")
Omega = E.period_lattice().omega()          # real period
print(Omega)
print()

print("=== Regulator (canonical height of generator) ===")
P = E.gens()[0]
Reg = P.height(precision=prec)
print(Reg)
print()

print("=== Analytic rank and L'(E,1) ===")
# Analytic rank + leading term
ar, lead = E.lseries().derivative_at_one(prec=prec)
print("Analytic rank =", ar)
print("L'(E,1)       =", lead)
print()

print("=== Strong BSD quotient ===")
prod_c = E.tamagawa_product()
tors2  = E.torsion_order()**2
RHS_Sha1 = Omega * Reg * 1 * prod_c / tors2
print("RHS assuming |Sha|=1 :", RHS_Sha1)
print("L'(E,1) / RHS        :", lead / RHS_Sha1)
print("Implied |Sha|        :", lead / (Omega * Reg * prod_c))