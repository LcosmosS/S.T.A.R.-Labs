from sage.all import EllipticCurve, QQ
E = EllipticCurve(QQ, [0, 0, 0, 2, 144])
   * print(dir(E))  # Check if 'heegner_points' is listed
