E2 = EllipticCurve(QQ, [0, 0, 0, 3, 1])
heegner = E2.heegner_point(-15)
P = heegner.point()
P_Q = P.trace_to_rational()
print(f"Traced Heegner point on E(Q): {P_Q}")
height = P_Q.height()
print(f"Height of the point: {height}")
if height > 0:
    print("The point is of infinite order, confirming rank >= 1")
else:


              ●       print("The point is a torsion point.")