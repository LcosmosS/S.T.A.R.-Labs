    return num_x, num_y

def predict_star_generator(r, rho, R=3.383, Omega=0.422, T=1, r=3):
    num_x, num_y = star_cosmic_recurrence(r, rho, R, Omega, T, r)
    d_x = 3**4  # 81
    d_y = 3**6  # 729
    return (QQ(num_x)/d_x, QQ(num_y)/d_y, 1)

# Cluster corpus
clusters = [
    ("Virgo", 54, 6200),
    ("Coma", 321, 9980),
