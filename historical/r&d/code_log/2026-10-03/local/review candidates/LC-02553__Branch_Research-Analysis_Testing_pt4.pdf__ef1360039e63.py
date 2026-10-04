# Define the pairs of coefficients for golden ratio-based curves, plus the original curve
pairs = [(1, 2), (2, 1), (3, 2), (5, 3), (-1706, 6320)]  # (a, b) pairs

# Loop over each pair to construct and analyze the curve
for a, b in pairs:
    print(f"\nCurve: y^2 = x^3 + {a}x + {b}")

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
    print(f"Torsion subgroup order: {tors_order}")
