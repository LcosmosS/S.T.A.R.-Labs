def predict_full_generator(r, rho):
    d_x = 3**4  # 81
    d_y = 3**6  # 729
    
    num_x = round(r * (10987 / 321))
    num_y = num_x * 70 + floor(rho / 3)
    
    return (QQ(num_x)/d_x, QQ(num_y)/d_y, 1)
