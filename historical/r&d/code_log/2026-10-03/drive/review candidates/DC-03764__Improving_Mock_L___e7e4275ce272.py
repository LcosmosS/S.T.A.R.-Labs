import numpy as np data = np.loadtxt("COM_PowerSpect_CMB-TT-full_R3.01.txt", skiprows=1) l = data[:, 0].astype(int) Cl = data[:, 1] # D_ℓ = ℓ(ℓ+1)C_ℓ/(2π) in μK^2
# Convert D_ℓ to C_ℓ
Cl = Cl * 2 * np.pi / (l * (l + 1)) with open("cl_tt.txt", "w") as f: f.write("C_l = [0, 0" + "".join([f", {Cl[i-2]}" for i in range(2, 2509)]) + "];")
