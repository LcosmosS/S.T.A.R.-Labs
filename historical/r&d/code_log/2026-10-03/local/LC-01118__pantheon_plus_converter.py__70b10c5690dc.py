import numpy as np
from astropy.io import fits
import json
import os

OUTPUT = "src/likelihoods/data/pantheon_plus_full.py"

def main():
    # Path to the official Pantheon+ FITS file
    fits_path = "data/pantheon_plus/Pantheon+SH0ES.fits"

    if not os.path.exists(fits_path):
        raise FileNotFoundError(
            f"Pantheon+ FITS file not found at {fits_path}. "
            "Download from: https://pantheonplussh0es.github.io/"
        )

    hdul = fits.open(fits_path)
    data = hdul[1].data

    z = data["zHD"].tolist()
    mu = data["MU"].tolist()
    sigma = data["MUERR"].tolist()

    with open(OUTPUT, "w") as f:
        f.write("# Auto-generated Pantheon+ full sample (1701 SNe)\n")
        f.write("# Do not edit manually.\n\n")
        f.write("PANTHEON_PLUS_FULL = {\n")
        f.write(f"  'z': {z},\n")
        f.write(f"  'mu': {mu},\n")
        f.write(f"  'sigma_mu': {sigma}\n")
        f.write("}\n")

    print(f"Pantheon+ dataset written to {OUTPUT}")

if __name__ == "__main__":
    main()
