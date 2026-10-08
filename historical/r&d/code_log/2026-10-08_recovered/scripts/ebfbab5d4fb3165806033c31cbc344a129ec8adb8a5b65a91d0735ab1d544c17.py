"""
Sky Projection Engine
=====================

Provides spherical projections for sky coordinates:
- Cartesian (unit sphere)
- Gnomonic
- Stereographic
- Aitoff

Used for embedding and visualization.
"""

from __future__ import annotations
import numpy as np


class SkyProjector:
    def __init__(self, projection="cartesian"):
        self.projection = projection

    def project(self, ra_deg, dec_deg):
        ra = np.deg2rad(ra_deg)
        dec = np.deg2rad(dec_deg)

        if self.projection == "cartesian":
            x = np.cos(dec) * np.cos(ra)
            y = np.cos(dec) * np.sin(ra)
            z = np.sin(dec)
            return np.vstack([x, y, z]).T

        if self.projection == "gnomonic":
            ra0 = 0
            dec0 = 0
            denom = np.sin(dec0)*np.sin(dec) + np.cos(dec0)*np.cos(dec)*np.cos(ra-ra0)
            x = np.cos(dec)*np.sin(ra-ra0) / denom
            y = (np.cos(dec0)*np.sin(dec) - np.sin(dec0)*np.cos(dec)*np.cos(ra-ra0)) / denom
            return np.vstack([x, y]).T

        if self.projection == "stereographic":
            x = 2 * np.cos(dec) * np.sin(ra/2)
            y = 2 * np.sin(dec)
            return np.vstack([x, y]).T

        if self.projection == "aitoff":
            alpha = (ra - np.pi) / 2
            denom = np.sqrt(1 + np.cos(dec) * np.cos(alpha))
            x = 2 * np.cos(dec) * np.sin(alpha) / denom
            y = np.sin(dec) / denom
            return np.vstack([x, y]).T

        raise ValueError(f"Unknown projection: {self.projection}")
