    else:
        print("The point is a torsion point.")
except Exception as e:
    print(f"Failed to compute Heegner point: {e}")

# Twist another curve to find more rank 3 curves (try a=987, b=377)
print("\nTwisting curve (a=987, b=377) to find a higher rank...")
d = -5  # Different twist
a_new = 987 * d
b_new = 377 * (d**3)
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

print(f"\nFinal training data: {training_data}")
print(f"Final labels: {training_labels}")
