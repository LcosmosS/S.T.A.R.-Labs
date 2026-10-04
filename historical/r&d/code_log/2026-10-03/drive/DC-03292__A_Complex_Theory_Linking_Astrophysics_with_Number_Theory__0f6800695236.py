# Define the elliptic curve
E = EllipticCurve(QQ, [-1706, 6320])  # y^2 = x^3 - 1706x + 6320 over QQ


# Compute the rank of the 2-Selmer group
S = E.selmer_rank(2)  # Compute the 2-Selmer rank (p=2)


# Print the 2-Selmer rank
print(S)


* E.selmer_rank(p) computes the rank of the ( p )-Selmer group, which for p = 2 is the 2-Selmer rank we’re interested in. This method is available in SageMath versions 8.0 and later, and it’s more robust than two_selmer_rank() in some contexts.
