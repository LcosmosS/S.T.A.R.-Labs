from astroquery.vizier import Vizier
import pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u

# Initialize Vizier with unlimited row limit
vizier = Vizier(columns=["*", "_RAJ2000", "_DEJ2000"], row_limit=-1)

# Step 1: Query NSA catalog
print("Querying NSA catalog (J/ApJ/896/10)...")
try:
    nsa_data = vizier.get_catalogs("J/ApJ/896/10")[0]
    nsa_df = nsa_data.to_pandas()
    print(f"NSA data loaded: {len(nsa_df)} rows.")
    print("NSA columns:", list(nsa_data.columns))
except Exception as e:
    raise ValueError(f"Failed to query NSA catalog. Error: {str(e)}")

# Step 2: Query xCOLD GASS catalog
print("Querying xCOLD GASS catalog (J/A+A/595/A43)...")
try:
    xcold_data = vizier.get_catalogs("J/A+A/595/A43")[0]
    xcold_df = xcold_data.to_pandas()
    print("xCOLD GASS columns:", list(xcold_data.columns))
    # Select RA, DEC, and molecular gas mass if available
    xcold_columns = ['_RAJ2000', '_DEJ2000']
    if 'logMH2' in xcold_data.columns:
        xcold_columns.append('logMH2')
    xcold_df = xcold_df[xcold_columns]
    print(f"xCOLD GASS data loaded: {len(xcold_df)} rows with columns {xcold_columns}.")
except Exception as e:
    print(f"Warning: Failed to load xCOLD GASS. Proceeding without it. Error: {str(e)}")
    xcold_df = pd.DataFrame()

# Step 3: Query Herschel catalog
print("Querying Herschel catalog (J/A+A/558/A133)...")
try:
    herschel_data = vizier.get_catalogs("J/A+A/558/A133")[0]
    herschel_df = herschel_data.to_pandas()
    print("Herschel columns:", list(herschel_data.columns))
    # Select RA, DEC, and dust mass if available
    herschel_columns = ['_RAJ2000', '_DEJ2000']
    if 'MDust' in herschel_data.columns:
        herschel_columns.append('MDust')
    herschel_df = herschel_df[herschel_columns]
    print(f"Herschel data loaded: {len(herschel_df)} rows with columns {herschel_columns}.")
except Exception as e:
    print(f"Warning: Failed to load Herschel. Proceeding without it. Error: {str(e)}")
    herschel_df = pd.DataFrame()

# Step 4: Cross-match NSA with xCOLD GASS if available
if not xcold_df.empty:
    print("Cross-matching NSA with xCOLD GASS...")
    nsa_coords = SkyCoord(ra=nsa_df['_RAJ2000']*u.deg, dec=nsa_df['_DEJ2000']*u.deg)
    xcold_coords = SkyCoord(ra=xcold_df['_RAJ2000']*u.deg, dec=xcold_df['_DEJ2000']*u.deg)
    idx, sep, _ = nsa_coords.match_to_catalog_sky(xcold_coords)
    matches = sep < 5 * u.arcsec
    merged_df = pd.concat([nsa_df[matches], xcold_df.iloc[idx[matches]].reset_index(drop=True)], axis=1)
else:
    merged_df = nsa_df.copy()

# Step 5: Cross-match with Herschel if available
if not herschel_df.empty:
    print("Cross-matching with Herschel...")
    merged_coords = SkyCoord(ra=merged_df['_RAJ2000']*u.deg, dec=merged_df['_DEJ2000']*u.deg)
    herschel_coords = SkyCoord(ra=herschel_df['_RAJ2000']*u.deg, dec=herschel_df['_DEJ2000']*u.deg)
    idx, sep, _ = merged_coords.match_to_catalog_sky(herschel_coords)
    matches = sep < 5 * u.arcsec
    final_df = pd.concat([merged_df[matches], herschel_df.iloc[idx[matches]].reset_index(drop=True)], axis=1)
else:
    final_df = merged_df.copy()

# Step 6: Finalize dataset
print("Final columns:", list(final_df.columns))
final_columns = ['_RAJ2000', '_DEJ2000']
if 'logMH2' in final_df.columns:
    final_columns.append('logMH2')
if 'MDust' in final_df.columns:
    final_columns.append('MDust')
final_df = final_df[final_columns].dropna()
print(f"Final dataset size: {len(final_df)} rows.")

# Step 7: Save to file
final_df.to_csv('sfr_prediction_dataset.csv', index=False)
print("Dataset saved to 'sfr_prediction_dataset.csv'.")