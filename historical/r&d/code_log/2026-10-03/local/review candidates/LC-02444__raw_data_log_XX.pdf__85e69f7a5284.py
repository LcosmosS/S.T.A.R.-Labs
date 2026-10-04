print(f"Expected: (10987/81 : 774964/729 : 1)")
print(f"Match: {P == (10987/81, 774964/729, 1)}")

# ———————— PREDICT NEW CLUSTER (e.g. Fornax) ————————
r_f, rho_f = 62, 3200
P_f = predict_full_generator(r_f, rho_f)
print(f"\nFornax Prediction (r={r_f}, ρ={rho_f}): {P_f}")
