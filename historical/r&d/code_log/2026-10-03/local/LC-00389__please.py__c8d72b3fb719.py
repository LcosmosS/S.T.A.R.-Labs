import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.coordinates import SkyCoord, match_coordinates_sky
import astropy.units as u
import os

# Paths and parameters
base_dir = os.path.expanduser("~/pmqr7")  # Adjust if files are elsewhere
spec_file = os.path.join(base_dir, "specObj-dr17.fits")
spall_file = os.path.join(base_dir, "spAllLine-v6_0_4.fits")
output_file = os.path.join(base_dir, "spectral_measurements.csv")
center_ra = 185.0  # degrees
center_dec = 32.5  # degrees
radius = 15.0      # degrees
match_tol = 5.0    # arcseconds
max_rows = 1200000 # 1.2M rows
chunk_size = 10000 # Rows per chunk

# Ensure output directory exists
os.makedirs(base_dir, exist_ok=True)

# Function to filter coordinates
def filter_coordinates(ra, dec, center_ra, center_dec, radius):
    coords = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, frame='icrs')
    center = SkyCoord(ra=center_ra*u.deg, dec=center_dec*u.deg, frame='icrs')
    separations = coords.separation(center).deg
    return separations <= radius

# 1. Process specObj-dr17.fits
print("Processing specObj-dr17.fits...")
df_spec_chunks = []
rows_processed = 0
try:
    with fits.open(spec_file, memmap=True) as spec_hdul:
        total_rows = len(spec_hdul[1].data)
        print(f"Total rows in specObj: {total_rows}")
        for start in range(0, min(max_rows, total_rows), chunk_size):
            end = min(start + chunk_size, max_rows)
            chunk = spec_hdul[1].data[start:end]
            rows_processed += len(chunk)
            
            ra = chunk['PLUG_RA']
            dec = chunk['PLUG_DEC']
            mask = filter_coordinates(ra, dec, center_ra, center_dec, radius)
            if not np.any(mask):
                print(f"Chunk {start}-{end}: No objects in 15° radius")
                continue
                
            chunk_filtered = pd.DataFrame({
                'RA_ICRS': ra[mask],
                'DE_ICRS': dec[mask],
                'zsp': chunk['Z'][mask],
                'flux_Ha': chunk.get('LINEFLUX_HA', np.zeros(len(chunk)))[mask],
                'flux_OIII_5007': chunk.get('LINEFLUX_OIII_5007', np.zeros(len(chunk)))[mask],
                'flux_HBETA': chunk.get('LINEFLUX_HBETA', np.zeros(len(chunk)))[mask],
                'flux_NII_6583': chunk.get('LINEFLUX_NII_6583', np.zeros(len(chunk)))[mask]
            })
            df_spec_chunks.append(chunk_filtered)
            
            print(f"Chunk {start}-{end}: Kept {len(chunk_filtered)}/{len(chunk)} objects")
            if rows_processed >= max_rows:
                break
                
except Exception as e:
    print(f"Error processing specObj: {e}")
    exit(1)

if not df_spec_chunks:
    print("No specObj objects within 15°")
    exit(1)

df_spec = pd.concat(df_spec_chunks, ignore_index=True)
print(f"Total specObj objects within 15°: {len(df_spec)}")

# 2. Process spAllLine-v6_0_4.fits
print("Processing spAllLine-v6_0_4.fits...")
df_spall_chunks = []
rows_processed = 0
try:
    with fits.open(spall_file, memmap=True) as spall_hdul:
        total_rows = len(spall_hdul[1].data)
        print(f"Total rows in spAllLine: {total_rows}")
        for start in range(0, min(max_rows, total_rows), chunk_size):
            end = min(start + chunk_size, max_rows)
            chunk = spall_hdul[1].data[start:end]
            rows_processed += len(chunk)
            
            ra = chunk['RA']
            dec = chunk['DEC']
            mask = filter_coordinates(ra, dec, center_ra, center_dec, radius)
            if not np.any(mask):
                print(f"Chunk {start}-{end}: No objects in 15° radius")
                continue
                
            chunk_filtered = pd.DataFrame({
                'RA_ICRS': ra[mask],
                'DE_ICRS': dec[mask],
                'flux_Ha_spall': chunk.get('HA_FLUX', np.zeros(len(chunk)))[mask],
                'flux_OIII_5007_spall': chunk.get('OIII_5007_FLUX', np.zeros(len(chunk)))[mask],
                'flux_HBETA_spall': chunk.get('HBETA_FLUX', np.zeros(len(chunk)))[mask],
                'flux_NII_6583_spall': chunk.get('NII_6583_FLUX', np.zeros(len(chunk)))[mask]
            })
            df_spall_chunks.append(chunk_filtered)
            
            print(f"Chunk {start}-{end}: Kept {len(chunk_filtered)}/{len(chunk)} objects")
            if rows_processed >= max_rows:
                break
                
except Exception as e:
    print(f"Error processing spAllLine: {e}")
    df_merged = df_spec
else:
    if not df_spall_chunks:
        print("No spAllLine objects within 15°")
        df_merged = df_spec
    else:
        df_spall = pd.concat(df_spall_chunks, ignore_index=True)
        print(f"Total spAllLine objects within 15°: {len(df_spall)}")

        # Cross-match
        print("Cross-matching specObj with spAllLine...")
        spec_coords = SkyCoord(ra=df_spec['RA_ICRS']*u.deg, dec=df_spec['DE_ICRS']*u.deg, frame='icrs')
        spall_coords = SkyCoord(ra=df_spall['RA_ICRS']*u.deg, dec=df_spall['DE_ICRS']*u.deg, frame='icrs')
        idx, sep2d, _ = match_coordinates_sky(spec_coords, spall_coords)
        match_mask = sep2d.arcsec <= match_tol

        df_spec_matched = df_spec[match_mask].copy()
        df_spall_matched = df_spall.iloc[idx[match_mask]].reset_index(drop=True)
        df_merged = pd.concat([df_spec_matched.reset_index(drop=True), 
                              df_spall_matched Aeneid
df_spall_matched[['flux_Ha_spall', 'flux_OIII_5007_spall', 
                                    'flux_HBETA_spall', 'flux_NII_6583_spall']]], axis=1)

        # Prioritize specObj fluxes
        for col in ['flux_Ha', 'flux_OIII_5007', 'flux_HBETA', 'flux_NII_6583']:
            df_merged[col] = df_merged[col].where(df_merged[col] != 0, df_merged[f'{col}_spall'])
            df_merged.drop(f'{col}_spall', axis=1, inplace=True)

# 3. Compute OH_O3N2_cen
print("Computing OH_O3N2_cen...")
valid_flux = (df_merged['flux_Ha'] > 0) & (df_merged['flux_OIII_5007'] > 0) & \
             (df_merged['flux_HBETA'] > 0) & (df_merged['flux_NII_6583'] > 0)
df_merged['OH_O3N2_cen'] = np.full(len(df_merged), 8.69)
df_merged.loc[valid_flux, 'OH_O3N2_cen'] = np.log10(
    (df_merged.loc[valid_flux, 'flux_OIII_5007'] / df_merged.loc[valid_flux, 'flux_HBETA']) /
    (df_merged.loc[valid_flux, 'flux_NII_6583'] / df_merged.loc[valid_flux, 'flux_Ha'])
)

# Drop temporary columns
df_merged.drop(['flux_OIII_5007', 'flux_HBETA', 'flux_NII_6583'], axis=1, inplace=True)

# 4. Save output
print("Saving output...")
df_merged.to_csv(output_file, index=False)
print(f"Saved {len(df_merged)} rows to {output_file}")
print(f"Output saved at: {os.path.abspath(output_file)}")