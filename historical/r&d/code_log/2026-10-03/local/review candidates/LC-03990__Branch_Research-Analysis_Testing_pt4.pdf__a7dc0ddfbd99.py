# Define the pairs of coefficients for pi-based curves, plus the original curve
pairs = [(3, 22), (22, 7), (333, 106), (355, 113), (-1706, 6320)]  # (a, b) pairs

# Loop over each pair to construct and analyze the curve
for a, b in pairs:
    print(f"\nCurve: y^2 = x^3 + {a}x + {b}")

    # Define the elliptic curve
    E = EllipticCurve(QQ, [a, b])

    # Compute the discriminant
    delta = E.discriminant()
    print(f"Discriminant: {delta}")
