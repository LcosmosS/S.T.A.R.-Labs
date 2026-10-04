import healpy as hp import numpy as np
# Load Planck 2018 TT power spectrum (example file)
cl = hp.read_cl("COM_PowerSpect_CMB-TT-full_R3.01.fits")[:2501] # Up to l=2500
# Export as PARI/GP vector
