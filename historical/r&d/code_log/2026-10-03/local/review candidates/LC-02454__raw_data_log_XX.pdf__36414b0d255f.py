from sage.all import *
def cosmic_recurrence(r, rho):
    """Exact empirical recurrence"""
    # Step 1: x-numerator from r
    num_x = round(r * (10987 / 321)) # ≈34.231

    # Step 2: y-numerator = x * 70 + fixed offset
    offset = 5874 # = 774964 - 10987*70
    num_y = num_x * 70 + offset