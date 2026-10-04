        for features, label in zip(training_data, training_labels):

            f.write(f"{features},{label}\n")

    print("Training data saved to selmer_training_data.txt")



# Heegner point analysis for selected curves

print("\n--- Heegner Point Analysis ---")

# Curve (a=34, b=-34), rank 2

print("\nAnalyzing curve (a=34, b=-34) for Heegner points...")
E1 = EllipticCurve(QQ, [0, 0, 0, 34, -34])

print(f"Curve: {E1}")

N1 = E1.conductor()

print(f"Conductor: {N1}")

try:

    heegner = E1.heegner_point(-7)

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



# Curve (a=3, b=1), rank 1, smaller conductor

print("\nAnalyzing curve (a=3, b=1) for Heegner points...")
E2 = EllipticCurve(QQ, [0, 0, 0, 3, 1])

print(f"Curve: {E2}")

N2 = E2.conductor()

print(f"Conductor: {N2}")
