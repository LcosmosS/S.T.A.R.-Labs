# Define the elliptic curve over the rational numbers (QQ)
E = EllipticCurve(QQ, [-1706, 6320])

# Calculate the discriminant of the curve E
delta = E.discriminant()
print(delta)

# Compute the torsion subgroup of E
torsion_subgroup = E.torsion_subgroup()
print(torsion_subgroup)

# Compute the algebraic rank of E
algebraic_rank = E.rank()
print(algebraic_rank)
