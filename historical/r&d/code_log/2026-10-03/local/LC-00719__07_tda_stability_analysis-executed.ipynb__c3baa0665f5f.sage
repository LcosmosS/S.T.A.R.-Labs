import sys, os
sys.path.append('src')
sys.path.append('../src')
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

import numpy as np, pandas as pd, matplotlib.pyplot as plt
np.random.seed(99)

os.makedirs('results', exist_ok=True)
