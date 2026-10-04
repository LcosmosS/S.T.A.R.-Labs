def cosmic_recurrence(r, rho):
    # Step 1: x-numerator
    num_x = round(r * (10987 / 321))  # = 10987
    
    # Step 2: y-numerator
    num_y = num_x * 70 + floor(rho / 3)
    
    return num_x, num_y
