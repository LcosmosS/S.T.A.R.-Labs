    n=1 → x, n=2 → y
    """
    if n == 1:
        # x-numerator: seed with r, scaled
        return floor(r * (rho // 100))  # heuristic: r * (ρ/100)
    else:
        # y-numerator: previous + recursive term
        prev = cosmic_numerator_seed(r, rho, n-1)
        return prev * 7 + floor(rho / (n + 1))  # 7 = empirical multiplier

def predict_generator(r, rho):
    """Predict full rational generator point from r, ρ"""
    # Denominators
    d_x = cosmic_denominator(1)
    d_y = cosmic_denominator(2)

    # Numerators
    num_x = cosmic_numerator_seed(r, rho, 1)
    num_y = cosmic_numerator_seed(r, rho, 2)

    # Construct point
    P_pred = (QQ(num_x)/QQ(d_x), QQ(num_y)/QQ(d_y), QQ(1))
    return P_pred, d_x, d_y, num_x, num_y

# ———————— TEST ON COMA CLUSTER ————————
r_coma = 321
