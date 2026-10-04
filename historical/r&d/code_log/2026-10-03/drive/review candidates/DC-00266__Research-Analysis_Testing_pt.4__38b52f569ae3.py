    training_labels.extend([0, 2])
    scaler = StandardScaler()
    X_train = scaler.fit_transform(training_data)
    y_train = [1 if label >= 3 else 0 for label in training_labels]
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)
    print(f"Classifier trained with available data. Coefficients: {clf.coef_}")
    with open("selmer_training_data.txt", "w") as f:
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
except Exception as e:
    print(f"Failed to compute rank of twisted curve: {e}")


# Final training data update
print("\nFinal training data: {training_data}")
print(f"Final labels: {training_labels}")


# Final classifier training
scaler = StandardScaler()
X_train = scaler.fit_transform(training_data)
y_train = [1 if label >= 3 else 0 for label in training_labels]
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)
print(f"Final classifier trained. Coefficients: {clf.coef_}")
with open("final_selmer_training_data.txt", "w") as f:
    for features, label in zip(training_data, training_labels):
        f.write(f"{features},{label}\n")
print("Final training data saved to final_selmer_training_data.txt")
