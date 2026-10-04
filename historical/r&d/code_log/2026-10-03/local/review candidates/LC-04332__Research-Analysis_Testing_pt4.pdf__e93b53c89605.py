try:

    heegner = E2.heegner_point(-23)

    P = heegner.point()

    P_Q = P.trace_to_rational()

    print(f"Traced Heegner point on E(Q): {P_Q}")

    height = P_Q.height()

    print(f"Height of the point: {height}")

    if height > 0:
        print("The point is of infinite order, confirming rank >= 1")

    else:

        print("The point is a torsion point.")

except Exception as e:

    print(f"Failed to compute Heegner point: {e}")



# Twist the curve (a=34, b=-34) to find a higher rank

print("\nTwisting curve (a=34, b=-34) to find a higher rank...")

d = -3

a_new = 34 * d

b_new = -34 * (d**3)

E_twist = EllipticCurve(QQ, [0, 0, 0, a_new, b_new])

print(f"Twisted curve: y² = x³ + {a_new}x + {b_new}")

try:

    rank_twist = E_twist.rank()

    print(f"Rank of twisted curve: {rank_twist}")

    if rank_twist >= 3:

        delta = E_twist.discriminant()

        conductor = E_twist.conductor()

        tors_order = E_twist.torsion_subgroup().order()
        features = [a_new, b_new, math.log(abs(delta)), math.log(conductor), tors_order]

        training_data.append(features)

        training_labels.append(rank_twist)

        print(f"Added twisted curve to training data: {features}, label: {rank_twist}")
