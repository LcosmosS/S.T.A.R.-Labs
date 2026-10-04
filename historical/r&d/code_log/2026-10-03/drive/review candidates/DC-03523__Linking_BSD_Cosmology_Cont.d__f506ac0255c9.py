import pandas as pd
import numpy as np
columns_to_keep = ['log_Mass', 'nsa_z', 'Re_kpc', 'ellip', 'log_Mass_gas', 'OH_Mar13_N2_Re_fit', 'vel_disp_ssp_1Re', 'u-g', 'g-r', 'V-band_SB_at_Re', 'zcomp_1Mpc', 'SFR_PETRORAD_R']
df = pd.read_csv('Pipe3D.csv')
