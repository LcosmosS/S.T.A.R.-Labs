# Define the elliptic curve
E = EllipticCurve(QQ, [-1706, 6320])


# Perform a 2-descent
info = E.two_descent(verbose=True)


# The 2-Selmer rank can be extracted from the two-descent information
# In older versions, this might be accessed via E.two_descent()[0] or similar
print(info)
