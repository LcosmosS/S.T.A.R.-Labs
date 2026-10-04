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