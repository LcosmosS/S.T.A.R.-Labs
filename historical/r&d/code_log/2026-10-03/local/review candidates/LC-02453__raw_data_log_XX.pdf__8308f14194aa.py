# ———————— TEST: COMA CLUSTER ————————
r, rho = 321, 9980
P = predict_full_generator(r, rho)
print(f"r = {r}, ρ = {rho}")
print(f"P = {P}")
print(f"Expected: (10987/81 : 774964/729 : 1)")
print(f"Match: {P == (10987/81, 774964/729, 1)}")

# ———————— TEST: FORNAX (hypothetical) ————————
r_f, rho_f = 62, 3200
P_f = predict_full_generator(r_f, rho_f)
print(f"\nFornax Prediction (r={r_f}, ρ={rho_f}): {P_f}")
