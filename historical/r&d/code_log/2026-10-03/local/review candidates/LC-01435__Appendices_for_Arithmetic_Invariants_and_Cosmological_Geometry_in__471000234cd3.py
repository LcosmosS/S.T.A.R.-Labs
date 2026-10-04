            if features not in training_data:
                training_data.append(features)
                training_labels.append(selmer3_rank)
                print(f"Found high 3-Selmer rank curve: a={a}, b={b}, 3-Selmer
rank={selmer3_rank}")
    gc.collect()
    attempt += 1

# Heegner Point Analysis
print("\n--- Heegner Point Analysis ---")
curves_for_heegner = [(34, -34, -11), (3, 1, -15)]
for a, b, D in curves_for_heegner:
    print(f"\nAnalyzing curve (a={a}, b={b}) for Heegner points...")
    E = EllipticCurve(QQ, [0, 0, 0, a, b])
    print(f"Curve: {E}")
    print(f"Conductor: {E.conductor()}")
    try:
        hp = heegner_points(E, D)
        print(f"Heegner point with D={D}: {hp}")
        if hp.has_finite_order():
            print("Point has finite order.")
        else:
            print(f"Point has infinite order with height: {hp.height()}")
    except Exception as e:
        print(f"Failed to compute Heegner point: {e}")
gc.collect()

# Twisting a curve
print("\n--- Twisting curve (a=34, b=-34) to find a higher rank... ---")
a_orig, b_orig, d = 34, -34, 5
a_twist, b_twist = a_orig * d**2, b_orig * d**3
print(f"Twisted curve: y² = x³ + {a_twist}x + {b_twist}")
result = analyze_curve(a_twist, b_twist, conductor_limit=1e14)
if len(result) == 10 and result[0]:
    _, features, rank_twist, _, _, _, _, _, _, _ = result
    print(f"Rank of twisted curve: {rank_twist}")
    if rank_twist >= 3:
        training_data.append(features)
        training_labels.append(rank_twist)
        print(f"Added twisted curve to training data: {features}, label:
