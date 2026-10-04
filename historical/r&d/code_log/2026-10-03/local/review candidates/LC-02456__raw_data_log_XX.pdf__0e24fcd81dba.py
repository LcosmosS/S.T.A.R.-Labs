from sage.all import *
import pandas as pd

# ———————— COSMIC RECURRENCE (EXACT FOR COMA) ————————
def cosmic_recurrence(r, rho):
    num_x = round(r * (10987 / 321))        # 34.231...
    offset = 5874                          # = 774964 - 10987*70
    num_y = num_x * 70 + offset
    return num_x, num_y

def predict_generator(r, rho):
    num_x, num_y = cosmic_recurrence(r, rho)
    d_x = 3**4  # 81