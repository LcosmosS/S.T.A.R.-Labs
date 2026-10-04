# SageMath Script Log 2: Torsion Subgroup, Generator, and Canonical Height
E = EllipticCurve(QQ, [-1706, 6320])

torsion = E.torsion_subgroup()
gens = E.gens()
P = E([2, 54])
reg = P.height(precision=100)          # correct keyword

print(f"Torsion Subgroup Structure: {torsion}")
print(f"Calculated Generators: {gens}")
print(f"Generator Point P Verification: {E.is_on_curve(2, 54)}")
print(f"High-Precision Regulator Reg(E) = height(P): {reg}")
