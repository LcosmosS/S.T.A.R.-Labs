import numpy as np data = np.loadtxt("COM_PowerSpect_CMB-TT-full_R3.01.txt", skiprows=1) l = data[:, 0].astype(int) Cl = data[:, 1] # C_l in μK^2
# PARI/GP vector (start at l=0, data from l=2)
