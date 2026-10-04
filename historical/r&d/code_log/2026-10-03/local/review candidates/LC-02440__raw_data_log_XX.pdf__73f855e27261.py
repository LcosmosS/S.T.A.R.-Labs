def cosmic_recurrence(r, rho):
    # Step 1: x-numerator (distance-scaled)
    num_x = round(r * (10987 / 321))  # 34.231...

    # Step 2: y-numerator (density-scaled multiplier)
    multiplier = rho / 142.0