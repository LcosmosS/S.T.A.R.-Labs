import pandas as pd
from astropy.coordinates import SkyCoord
from astropy import units as u

# Step 1: Merge the mapping with SDSS_MangaSpec_with_fluxes.csv
# The output you provided as a DataFrame
mapping_data = {
    'SpecObjID': [
        1566278825162074112, 1623645848250378240, 1764322865512998912,
        2641484114523351040, 2814764680608770048
    ],
    'objID': [
        1237662306736472254, 1237661358077116708, 1237662663760806446,
        1237667209980608740, 1237667917025837162
    ],
    'ra': [239.742017, 171.041017, 254.278807, 154.621726, 172.475485],
    'dec': [27.987424, 47.144774, 17.344327, 25.289831, 20.678795]
}
mapping_df = pd.DataFrame(mapping_data)

# Load SDSS_MangaSpec_with_fluxes.csv and merge
manga = pd.read_csv("SDSS_MangaSpec_with_fluxes.csv")
manga_with_coords = manga.merge(mapping_df, left_on='SpecObj', right_on='SpecObjID', how='left')
manga_with_coords.to_csv("SDSS_MangaSpec_with_fluxes_with_coords.csv", index=False)

# Step 2: Check RA/Dec ranges for all datasets
sdssdr16_files = [
    "ALLWISE_SDSSDR16.csv", "TwoMass_SDSSDR16.csv", "STARHORSE2021_SDSSDR16.csv",
    "GALAXGR6+7AIS_SDSSDR16.csv", "UKIDSSDR9LAS_SDSSDR16.csv", "GAIADR3AP_SDSSDR16.csv",
    "PanST2DR1_SDSSDR16.csv", "PanSTDR1_SDSSDR16.csv"
]

# Check RA/Dec for SDSS_MangaSpec_with_fluxes_with_coords.csv
print("\nRA/Dec ranges for SDSS_MangaSpec_with_fluxes_with_coords.csv:")
print(f"RA: {manga_with_coords['ra'].min()} to {manga_with_coords['ra'].max()}")
print(f"Dec: {manga_with_coords['dec'].min()} to {manga_with_coords['dec'].max()}")

# Check RA/Dec for merged_galspec_gz2.csv
gz2 = pd.read_csv("merged_galspec_gz2.csv")
print("\nRA/Dec ranges for merged_galspec_gz2.csv:")
print(f"RA: {gz2['ra'].min()} to {gz2['ra'].max()}")
print(f"Dec: {gz2['dec'].min()} to {gz2['dec'].max()}")

# Check RA/Dec for _SDSSDR16 files
for file in sdssdr16_files:
    print(f"\nChecking RA/Dec ranges for {file}...")
    try:
        df = pd.read_csv(file, usecols=['RA_ICRS', 'DE_ICRS'])
        print(f"RA: {df['RA_ICRS'].min()} to {df['RA_ICRS'].max()}")
        print(f"Dec: {df['DE_ICRS'].min()} to {df['DE_ICRS'].max()}")
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Step 3: Coordinate-based merge with _SDSSDR16 files
# For SDSS_MangaSpec_with_fluxes_with_coords.csv
# Drop rows with NaN RA/Dec to avoid errors in SkyCoord
manga_with_coords = manga_with_coords.dropna(subset=['ra', 'dec'])
manga_coords = SkyCoord(ra=manga_with_coords['ra'].values*u.deg, dec=manga_with_coords['dec'].values*u.deg)

for file in sdssdr16_files:
    print(f"\nMerging SDSS_MangaSpec_with_fluxes_with_coords.csv with {file}...")
    try:
        df = pd.read_csv(file, usecols=['RA_ICRS', 'DE_ICRS', 'umag', 'gmag', 'rmag', 'imag', 'zmag'])
        df_coords = SkyCoord(ra=df['RA_ICRS'].values*u.deg, dec=df['DE_ICRS'].values*u.deg)
        
        idx, d2d, _ = manga_coords.match_to_catalog_sky(df_coords)
        max_sep = 1.0 * u.arcsec
        matches = d2d < max_sep
        
        manga_matched = manga_with_coords.iloc[matches].copy()
        df_matched = df.iloc[idx[matches]].copy()
        merged_df = pd.concat([manga_matched.reset_index(drop=True), df_matched.reset_index(drop=True)], axis=1)
        
        print(f"Number of matches: {len(merged_df)}")
        if len(merged_df) > 0:
            print(merged_df.head().to_string(index=False))
        
    except Exception as e:
        print(f"Error merging with {file}: {e}")

# For merged_galspec_gz2.csv (assuming we already have it; if not, use the previous script to pull from SDSS)
gz2_coords = SkyCoord(ra=gz2['ra'].values*u.deg, dec=gz2['dec'].values*u.deg)

for file in sdssdr16_files:
    print(f"\nMerging merged_galspec_gz2.csv with {file}...")
    try:
        df = pd.read_csv(file, usecols=['RA_ICRS', 'DE_ICRS', 'umag', 'gmag', 'rmag', 'imag', 'zmag'])
        df_coords = SkyCoord(ra=df['RA_ICRS'].values*u.deg, dec=df['DE_ICRS'].values*u.deg)
        
        idx, d2d, _ = gz2_coords.match_to_catalog_sky(df_coords)
        max_sep = 1.0 * u.arcsec
        matches = d2d < max_sep
        
        gz2_matched = gz2.iloc[matches].copy()
        df_matched = df.iloc[idx[matches]].copy()
        merged_df = pd.concat([gz2_matched.reset_index(drop=True), df_matched.reset_index(drop=True)], axis=1)
        
        print(f"Number of matches: {len(merged_df)}")
        if len(merged_df) > 0:
            print(merged_df.head().to_string(index=False))
        
    except Exception as e:
        print(f"Error merging with {file}: {e}")