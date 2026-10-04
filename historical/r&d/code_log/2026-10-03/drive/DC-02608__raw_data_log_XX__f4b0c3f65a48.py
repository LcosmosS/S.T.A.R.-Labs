def cosmic_recurrence(r, rho):
    # Step 1: x-numerator (distance-scaled)
    num_x = round(r * (10987 / 321))  # 34.231...
    
    # Step 2: y-numerator (density-scaled multiplier)
    multiplier = rho / 142.0
    num_y = round(num_x * multiplier)
    
    return num_x, num_y
