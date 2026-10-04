import numpy as np
# Load TT spectrum (example format: l, Cl, error_low, error_high)
data = np.loadtxt("COM_PowerSpect_CMB-TT-full_R3.01.txt", skiprows=1) l = data[:, 0].astype(int) Cl = data[:, 1] # C_l in μK^2
# Export for PARI/GP (l=1 has no data, start at l=2)
