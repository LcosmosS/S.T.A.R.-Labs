from astropy.coordinates import SkyCoord
from astropy import units as u
import pandas as pd


# Example: Load GAMA and SDSS/MaNGA datasets
gama_df = pd.read_csv('GAMA_dataset.csv')      # Has RA/DEC, CATAID
sdss_df = pd.read_csv('SDSS_dataset.csv')      # Has RA/DEC, plateifu


# Convert to SkyCoord for matching
gama_coords = SkyCoord(ra=gama_df['RA']*u.degree, dec=gama_df['DEC']*u.degree)
sdss_coords = SkyCoord(ra=sdss_df['RA']*u.degree, dec=sdss_df['DEC']*u.degree)


# Match with 1 arcsecond tolerance
idx, d2d, _ = sdss_coords.match_to_catalog_sky(gama_coords)
match_mask = d2d.arcsecond < 1.0


# Build matched dataframe
matched_sdss = sdss_df[match_mask].reset_index(drop=True)
matched_gama = gama_df.iloc[idx[match_mask]].reset_index(drop=True)


# Merge matched sets
merged_df = pd.concat([matched_sdss, matched_gama], axis=1)
