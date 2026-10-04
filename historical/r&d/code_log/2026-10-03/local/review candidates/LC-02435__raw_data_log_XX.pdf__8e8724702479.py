    num_x = cosmic_numerator_seed(r, rho, 1)
    num_y = cosmic_numerator_seed(r, rho, 2)

    # Construct point
    P_pred = (QQ(num_x)/QQ(d_x), QQ(num_y)/QQ(d_y), QQ(1))

    return P_pred, d_x, d_y, num_x, num_y

# ———————— TEST ON COMA CLUSTER ————————

r_coma = 321
rho_coma = 9980
P_pred, d_x, d_y, num_x, num_y = predict_generator(r_coma, rho_coma)
print("=== COMA CLUSTER PREDICTION ===")
print(f"Input: r = {r_coma}, ρ = {rho_coma}")
print(f"Predicted denom_x = 3^4 = {d_x}")
print(f"Predicted denom_y = 3^6 = {d_y}")
print(f"Predicted num_x = {num_x}")
print(f"Predicted num_y = {num_y}")
print(f"Predicted P = ({num_x}/{d_x} : {num_y}/{d_y} : 1)")

print(f"Actual P = (10987/81 : 774964/729 : 1)")

# ———————— VALIDATE CURVE ————————

a = -round(31.59259259259259 * r_coma)
b = rho_coma
E = EllipticCurve(QQ, [a, b])
rank = E.rank()
gens = E.gens()
print("\n=== CURVE VALIDATION ===")
print(f"Curve: y² = x³ + {a}x + {b}")
print(f"Rank: {rank}")
if rank > 0:
    print(f"Actual Generator: {gens[0]}")
    print(f"Match? {P_pred == gens[0]}")
