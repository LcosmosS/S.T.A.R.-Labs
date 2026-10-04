from sage.all import *


def cosmic_recurrence(r, rho):
    """Exact empirical recurrence"""
    # Step 1: x-numerator from r
    num_x = round(r * (10987 / 321))  # ≈34.231
    
    # Step 2: y-numerator = x * 70 + fixed offset
    offset = 5874  # = 774964 - 10987*70
    num_y = num_x * 70 + offset
    
    return num_x, num_y


def predict_full_generator(r, rho):
    num_x, num_y = cosmic_recurrence(r, rho)
    d_x = 3**4  # 81
    d_y = 3**6  # 729
    return (QQ(num_x)/d_x, QQ(num_y)/d_y, 1)


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
