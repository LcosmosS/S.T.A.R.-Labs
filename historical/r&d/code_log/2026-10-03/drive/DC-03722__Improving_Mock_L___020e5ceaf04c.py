import numpy as np
data = np.loadtxt("COM_PowerSpect_CMB-TT-full_R3.01.txt", skiprows=1)
l = data[:, 0].astype(int)
Cl = data[:, 1]  # D_ℓ = ℓ(ℓ+1)C_ℓ/(2π) in μK^2
# Convert D_ℓ to C_ℓ
Cl = Cl * 2 * np.pi / (l * (l + 1))
with open("cl_tt.txt", "w") as f:
   *     f.write("C_l = [0, 0" + "".join([f", {Cl[i-2]}" for i in range(2, 2509)]) + "];")
   * Redefine in PARI/GP:
   * pari
T_cmb = 2.7255e6; /* CMB temperature in μK */
read("cl_tt.txt"); /* Planck TT C_l */
   * L_cosmo(s) = sum(n=2, 2508, (C_l[n] / T_cmb^2) / n^s);
* Adjustment: The unscaled sum is small due to C_\ell / T_{\text{cmb}}^2 \approx 10^{-10} to 10⁻⁷. Add a scaling factor ( K ):
* pari
unscaled = sum(n=2, 2508, (C_l[n] / T_cmb^2) / n);
print("Unscaled L_cosmo(1): ", unscaled);
K = 1.0 / unscaled; /* Target ~1 */
* L_cosmo(s) = K * sum(n=2, 2508, (C_l[n] / T_cmb^2) / n^s);
