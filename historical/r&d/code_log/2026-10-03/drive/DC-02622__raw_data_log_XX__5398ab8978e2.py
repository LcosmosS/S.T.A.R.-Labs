# robust_cluster_test.py
from sage.all import *
import pandas as pd


def normalize_point(P):
    if P is None: return None
    x, y, z = P
    return (x/z, y/z, 1) if z != 0 else P


def cosmic_recurrence(r, rho):
    num_x = round(r * (10987 / 321))
    offset = 5874
    num_y = num_x * 70 + offset
    return num_x, num_y


def predict_generator(r, rho):
    num_x, num_y = cosmic_recurrence(r, rho)
    d_x = 3**4
    d_y = 3**6
    return (QQ(num_x)/d_x, QQ(num_y)/d_y, 1)


def derive_curve(r, rho, kappa=31.59259259259259):
    a = -round(kappa * r)
    b = rho
    return a, b


clusters = [
    ("Virgo", 54, 6200),
    ("Coma", 321, 9980),
