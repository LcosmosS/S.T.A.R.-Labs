    sizes = [float(max(x[3] * 100, 1e-6)) for x in interweb_data]
    colors = [x[7] for x in interweb_data]
    scatter = ax.scatter(log_deltas, log_conds, ranks, s=sizes, c=colors, cmap='viridis', alpha=0.7)
    plt.colorbar(scatter, label='Weak BSD Holds')
    for i in range(len(interweb_data)):
        for j in range(i + 1, len(interweb_data)):
            reg_diff = abs(interweb_data[i][5] - interweb_data[j][5])
            if reg_diff < 10000:
                weight = 1 / (1 + reg_diff / 100)
                ax.plot([log_deltas[i], log_deltas[j]], [log_conds[i], log_conds[j]], [ranks[i], ranks[j]], 'b-', alpha=0.5 * weight, linewidth=0.7 * weight)
        if interweb_data[i][2] >= 2:
            color = 'red' if interweb_data[i][2] == 3 else 'blue'
            ax.text(log_deltas[i], log_conds[i], ranks[i], f'({interweb_data[i][0]},{interweb_data[i][1]}): 54.0 Mly', size=8, color=color)
    ax.set_xlabel('Log(Discriminant)')
    ax.set_ylabel('Log(Conductor)')
    ax.set_zlabel('Rank')
    ax.set_title('Cosmic Interweb: Nodes and Weighted Filaments')
    plt.savefig("interweb_final.png")
    plt.close()
    print("Cosmic interweb plot saved as interweb_final.png")
except Exception as e:
    print(f"Failed to generate interweb plot: {e}")


# Heegner point analysis with corrected discriminants
print("\n--- Heegner Point Analysis ---")
# Curve (a=34, b=-34), D = -11
print("\nAnalyzing curve (a=34, b=-34) for Heegner points...")
E1 = EllipticCurve(QQ, [0, 0, 0, 34, -34])
print(f"Curve: {E1}")
N1 = E1.conductor()
print(f"Conductor: {N1}")
try:
    heegner = E1.heegner_point(-11)
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


# Curve (a=3, b=1), D = -15
print("\nAnalyzing curve (a=3, b=1) for Heegner points...")
E2 = EllipticCurve(QQ, [0, 0, 0, 3, 1])
print(f"Curve: {E2}")
N2 = E2.conductor()
print(f"Conductor: {N2}")
try:
    heegner = E2.heegner_point(-15)
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
