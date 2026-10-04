    d_y = 3**6  # 729
    return (QQ(num_x)/d_x, QQ(num_y)/d_y, 1)

def derive_curve(r, rho, kappa=31.59259259259259):
    a = -round(kappa * r)
    b = rho
    return a, b

# ———————— CLUSTER CORPUS ————————
clusters = [
    ("Virgo",      54,  6200),
    ("Coma",      321, 9980),
