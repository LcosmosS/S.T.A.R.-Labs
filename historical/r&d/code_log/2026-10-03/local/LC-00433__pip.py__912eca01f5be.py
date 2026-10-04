import pandas as pd
import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u
from scipy.spatial import cKDTree

# --- Load datasets ---
sdss = pd.read_csv("SDSSDR18_200000.csv", usecols=["objid", "ra", "dec"])
manga = pd.read_csv("mangaHIall.csv", usecols=["MANGAID", "OBJRA", "OBJDEC"])

# --- Convert to SkyCoord ---
sdss_coords = SkyCoord(ra=sdss["ra"].values * u.degree, dec=sdss["dec"].values * u.degree)
manga_coords = SkyCoord(ra=manga["OBJRA"].values * u.degree, dec=manga["OBJDEC"].values * u.degree)

# --- Build KDTree and query ---
manga_tree = cKDTree(np.column_stack((manga_coords.ra.rad, manga_coords.dec.rad)))
sdss_points = np.column_stack((sdss_coords.ra.rad, sdss_coords.dec.rad))

# Match within 2 arcseconds
max_sep = (2.0 * u.arcsec).to(u.radian).value
dist_rad, idx = manga_tree.query(sdss_points, distance_upper_bound=max_sep)

# Filter valid matches
matched = dist_rad != np.inf
matched_sdss = sdss[matched].reset_index(drop=True)
matched_manga = manga.iloc[idx[matched]].reset_index(drop=True)

# Compute arcsec separation
separation_arcsec = dist_rad[matched] * u.radian.to(u.arcsec)

# --- Merge matched DataFrames ---
merged = pd.concat([matched_sdss, matched_manga], axis=1)
merged["arcsec_separation"] = separation_arcsec

# Save the merged file
merged.to_csv("merged_sdssdr18_mangaHI_kdtree.csv", index=False)

# Preview
print(f"Merged {len(merged)} entries within 2 arcsec.")
print(merged.head())
