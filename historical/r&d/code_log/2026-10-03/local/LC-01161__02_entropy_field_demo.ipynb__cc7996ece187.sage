import sys, os

sys.path.append("src")
sys.path.append("../src")
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

import numpy as np, pandas as pd, matplotlib.pyplot as plt

np.random.seed(42)

print("NumPy:", np.__version__)
os.makedirs("results", exist_ok=True)