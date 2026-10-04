# Define the elliptic curve
E = EllipticCurve(QQ, [a, b])

# Compute the discriminant
delta = E.discriminant()
print(f"Discriminant: {delta}")
if delta == 0:
    print("Not an elliptic curve (singular). Skipping.")
    continue

# Compute the conductor
conductor = E.conductor()
print(f"Conductor: {conductor}")

# Compute the torsion subgroup
tors = E.torsion_subgroup()
tors_order = tors.order()