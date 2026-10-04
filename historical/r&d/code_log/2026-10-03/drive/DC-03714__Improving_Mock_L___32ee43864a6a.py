import healpy as hp
import numpy as np
# Load Planck 2018 TT power spectrum (example file)
cl = hp.read_cl("COM_PowerSpect_CMB-TT-full_R3.01.fits")[:2501]  # Up to l=2500
# Export as PARI/GP vector
with open("cl_vector.txt", "w") as f:
   *     f.write("C_l = [0, 0" + "".join([f", {cl[i]}" for i in range(2, 2501)]) + "];")
   * In PARI/GP:
   * pari
T_cmb = 2.7255e6; /* μK */
read("cl_vector.txt"); /* Load real C_l data */
   * L_cosmo(s) = 1e4 * sum(n=2, 2500, (C_l[n] / T_cmb^2) / n^s);
* Benefit: Captures the true CMB fluctuations, making L_{\text{cosmo}}(1) a more accurate cosmological analogue to the BSD L-function.
