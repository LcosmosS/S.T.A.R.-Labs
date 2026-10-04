import pandas as pd
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u

# Step 1: Load the datasets
print("Loading datasets...")
sdss_dr18 = pd.read_csv("SDSSDR18_200000.csv")
gzh = pd.read_csv("gz_hubble_sdss_coadd.csv")

# Step 2: Filter SDSS DR18 to the Stripe 82 region and galaxies
print("Filtering SDSS DR18 to Stripe 82 region and galaxies...")
# Stripe 82: RA ~310° to 60° (wrapping around 0°), DEC from -1.25° to 1.25°
sdss_dr18['RA_wrapped'] = sdss_dr18['ra'].apply(lambda x: x if x < 60 else x - 360)
stripe82_mask = (
    ((sdss_dr18['RA_wrapped'] >= -50) | (sdss_dr18['RA_wrapped'] <= 60)) &
    (sdss_dr18['dec'] >= -1.25) & (sdss_dr18['dec'] <= 1.25) &
    (sdss_dr18['class'] == 'GALAXY') &  # Filter for galaxies
    (sdss_dr18['redshift'] < 0.4)  # Filter for low-redshift galaxies
)
sdss_dr18_stripe82 = sdss_dr18[stripe82_mask].copy()
print(f"SDSS DR18 rows in Stripe 82 (galaxies, z < 0.4): {len(sdss_dr18_stripe82)}")

# Step 3: Perform positional cross-match
print("Performing positional cross-match...")
sdss_coords = SkyCoord(
    ra=sdss_dr18_stripe82['ra'].values * u.deg,
    dec=sdss_dr18_stripe82['dec'].values * u.deg
)
gzh_coords = SkyCoord(
    ra=gzh['RA'].values * u.deg,
    dec=gzh['DEC'].values * u.deg
)

# Find the closest matches within 1 arcsecond
max_separation = 1.0 * u.arcsec
idx, d2d, _ = sdss_coords.match_to_catalog_sky(gzh_coords)
separation = d2d.to(u.arcsec)
match_mask = separation < max_separation

# Step 4: Merge the datasets
print("Merging datasets...")
sdss_matched = sdss_dr18_stripe82[match_mask].reset_index(drop=True)
gzh_matched = gzh.iloc[idx[match_mask]].reset_index(drop=True)
sdss_matched['match_separation_arcsec'] = separation[match_mask].value
merged_df = pd.concat([sdss_matched, gzh_matched], axis=1)

# Step 5: Save the merged dataset
print(f"Merged dataset has {len(merged_df)} rows.")
merged_df.to_csv("sdss_dr18_gzh_merged.csv", index=False)
print("Merged dataset saved as 'sdss_dr18_gzh_merged.csv'.")