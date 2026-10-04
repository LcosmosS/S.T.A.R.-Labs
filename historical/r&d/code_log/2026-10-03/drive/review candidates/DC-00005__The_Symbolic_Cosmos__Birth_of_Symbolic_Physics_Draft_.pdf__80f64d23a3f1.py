# Define the elliptic curve E derived from our cosmological model.
# The coefficients a and b were derived from cosmic data.
E = EllipticCurve(QQ, [-1706, 6320])
# Our theory predicts a rank of 1.
# We will use the gens() function to find the single generator P.
# This generator represents the key "building block" of our curve's rational points.
P = E.gens()[0]
print(f"The generator of the curve is: {P}")
