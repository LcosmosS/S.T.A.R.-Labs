E = EllipticCurve('11a1')  # Cremona label for a rank 0 curve
print(E.rank())  # Should be 0
print(E.L_value(1))  # Compute L(E, 1)
* print(E.sha().an())  # Analytic order of Sha
* Compare these values to confirm the normalization.
