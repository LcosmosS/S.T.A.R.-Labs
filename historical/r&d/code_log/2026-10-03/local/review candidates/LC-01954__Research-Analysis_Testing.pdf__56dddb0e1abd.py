# Define the elliptic curve
E = EllipticCurve(QQ, [-1706, 6320]) # y^2 = x^3 - 1706x + 6320 over QQ
# Compute the rank of the 2-Selmer group
S = E.two_selmer_rank()
# Print the 2-Selmer rank
print(S)
