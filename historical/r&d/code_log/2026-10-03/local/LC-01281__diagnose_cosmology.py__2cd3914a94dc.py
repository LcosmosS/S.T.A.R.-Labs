import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.physics.cosmology import Cosmology
from src.physics.symbolic_cosmology import SymbolicCosmology


def run():
    lcdm = Cosmology("H0*sqrt(Ωm*(1+z)**3 + ΩΛ)", {"H0": 70, "Ωm": 0.3, "ΩΛ": 0.7})
    star = SymbolicCosmology(
        "H0*sqrt(Ωm*(1+z)**3 + ΩΛ + a*z + b*z**2)",
        {"H0": 70, "Ωm": 0.3, "ΩΛ": 0.7, "a": -0.05, "b": 0.01},
    )

    print("lcdm.params:", lcdm.params)
    print("star.params:", star.params)

    zgrid = np.linspace(0.0, 2.0, 201)
    try:
        Hz_lcdm = lcdm.H_of_z(zgrid)
        print(
            "lcdm H: min, max, any non-finite, any <=0 ->",
            np.min(Hz_lcdm),
            np.max(Hz_lcdm),
            np.any(~np.isfinite(Hz_lcdm)),
            np.any(Hz_lcdm <= 0),
        )
    except Exception as e:
        print("lcdm H_of_z raised:", repr(e))

    try:
        Hz_star = star.H_of_z(zgrid)
        print(
            "star  H: min, max, any non-finite, any <=0 ->",
            np.min(Hz_star),
            np.max(Hz_star),
            np.any(~np.isfinite(Hz_star)),
            np.any(Hz_star <= 0),
        )
    except Exception as e:
        print("star H_of_z raised:", repr(e))

    def find_first_bad(model, name):
        for zi in zgrid:
            try:
                Dc = model.comoving_distance(float(zi))
                DL = model.luminosity_distance(float(zi))
            except Exception as e:
                print(f"{name}: exception at z={zi} -> {e!r}")
                return
            if not np.isfinite(Dc) or not np.isfinite(DL) or DL <= 0:
                print(f"{name}: bad result at z={zi} Dc={Dc} DL={DL}")
                return
        print(f"{name}: all z in grid OK")

    find_first_bad(lcdm, "lcdm")
    find_first_bad(star, "star")


if __name__ == "__main__":
    run()
