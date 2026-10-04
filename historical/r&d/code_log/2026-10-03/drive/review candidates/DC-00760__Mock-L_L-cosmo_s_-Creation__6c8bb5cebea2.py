import numpy as np


# Load TT spectrum
data_tt = np.loadtxt("COM_PowerSpect_CMB-TT-full_R3.01.txt", skiprows=1)
l_tt = data_tt[:, 0].astype(int)
Cl_tt = data_tt[:, 1]  # C_l in μK^2


# Load TE spectrum
data_te = np.loadtxt("COM_PowerSpect_CMB-TE-full_R3.01.txt", skiprows=1)
Cl_te = data_te[:, 1]


# Load EE spectrum
data_ee = np.loadtxt("COM_PowerSpect_CMB-EE-full_R3.01.txt", skiprows=1)
Cl_ee = data_ee[:, 1]


# Export as PARI/GP vectors (start at l=0, data from l=2)
with open("cl_tt.txt", "w") as f:
    f.write("C_l_tt = [" + ", ".join(["0"] * 2 + [str(Cl_tt[i-2]) for i in range(2, 2509)]) + "];")
with open("cl_te.txt", "w") as f:
    f.write("C_l_te = [" + ", ".join(["0"] * 2 + [str(Cl_te[i-2]) for i in range(2, 1997)]) + "];")
with open("cl_ee.txt", "w") as f:
