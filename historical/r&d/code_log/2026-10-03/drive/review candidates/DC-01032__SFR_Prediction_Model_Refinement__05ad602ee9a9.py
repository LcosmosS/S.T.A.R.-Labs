from astropy.coordinates import SkyCoord
from astropy import units as u
import pandas as pd


# Load data
sdss_df = pd.read_csv('SDSS18_200000.csv')
gema_df = pd.read_csv('gema_data.csv')


# Rename RA/Dec to standard names for easier matching
sdss_df.rename(columns={'ra': 'RA', 'dec': 'DEC'}, inplace=True)
gema_df.rename(columns={'objra': 'RA', 'objdec': 'DEC'}, inplace=True)


# Create SkyCoord objects
coords_sdss = SkyCoord(ra=sdss_df['RA'].values * u.degree, dec=sdss_df['DEC'].values * u.degree)
coords_gema = SkyCoord(ra=gema_df['RA'].values * u.degree, dec=gema_df['DEC'].values * u.degree)


# Match SDSS to GEMA (1 arcsec tolerance)
idx, d2d, _ = coords_sdss.match_to_catalog_sky(coords_gema)
match_mask = d2d.arcsecond < 1.0


# Build matched DataFrame
matched_sdss = sdss_df[match_mask].reset_index(drop=True)
matched_gema = gema_df.iloc[idx[match_mask]].reset_index(drop=True)


# Combine matched rows
merged_df = pd.concat([matched_sdss, matched_gema], axis=1)
print(f"Merged dataframe: {merged_df.shape}")


# Save for later use
merged_df.to_csv('merged_sdss_gema.csv', index=False)
