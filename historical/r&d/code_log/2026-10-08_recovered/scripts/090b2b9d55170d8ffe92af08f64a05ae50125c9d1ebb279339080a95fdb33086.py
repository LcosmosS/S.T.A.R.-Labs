import pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u

# Step 1: Load catalogs
print("Loading catalogs...")
try:
    manga = pd.read_csv('SDSS_MangaSpec_with_fluxes.csv')
except FileNotFoundError:
    print("Error: SDSS_MangaSpec_with_fluxes.csv not found.")
    exit(1)

try:
    galspec_gz2 = pd.read_csv('merged_galspec_gz2.csv')
except FileNotFoundError:
    print("Error: merged_galspec_gz2.csv not found.")
    exit(1)

print(f"SDSS_MangaSpec_with_fluxes: {len(manga)} rows")
print(f"merged_galspec_gz2: {len(galspec_gz2)} rows")

# Step 2: Merge on SpecObj/objid
print("Merging on SpecObj/objid...")
manga['SpecObj'] = manga['SpecObj'].astype(str)
galspec_gz2['objid'] = galspec_gz2['objid'].astype(str)

merged = pd.merge(manga, galspec_gz2, left_on='SpecObj', right_on='objid', 
                  how='outer', suffixes=('_manga', '_galspec'))

# Step 3: Handle coordinates and columns
print("Consolidating columns...")
# If ra/dec exist in manga (not in sample), consolidate
if 'ra_manga' in merged.columns and 'dec_manga' in merged.columns:
    merged['ra'] = merged['ra_manga'].fillna(merged['ra_galspec'])
    merged['dec'] = merged['dec_manga'].fillna(merged['dec_galspec'])
    merged = merged.drop(columns=['ra_manga', 'dec_manga', 'ra_galspec', 'dec_galspec'])
else:
    # Use galspec ra/dec if manga lacks them
    merged['ra'] = merged['ra_galspec']
    merged['dec'] = merged['dec_galspec']
    merged = merged.drop(columns=['ra_galspec', 'dec_galspec'], errors='ignore')

# Rename for *S.T.A.R.* compatibility
merged = merged.rename(columns={
    'z': 'zsp',
    'logmass': 'logMass',
    'petrorad_r': 'kronRad',
    'ra': 'objra_y',
    'dec': 'objdec'
})

# Step 4: Save output
output_file = 'merged_manga_galspec_gz2.csv'
merged.to_csv(output_file, index=False)
print(f"Merged catalog saved as '{output_file}' with {len(merged)} rows")
print("Columns:", merged.columns.tolist())