import pandas as pd

# Load the new GZ dataset (GZ_410166.csv) and check the column names
gzoo = pd.read_csv("GZ_410166.csv")
gzoo['objid'] = gzoo['objID'].astype(str)  # Convert 'objID' to 'objid'
gzoo = gzoo.drop(columns=['objID'])  # Drop the 'objID' column after renaming

# Load all other datasets
core = pd.read_csv("merged_sdss_hi_with_arcsec.csv")  # Existing dataset with arcsec
magphys = pd.read_csv("MagPhys.csv")  # Include objid
stellar_mass = pd.read_csv("StellarMassesLambdar.csv")  # Includes CATAID
galaxy_classified = pd.read_csv("GalaxiesClassified.csv")  # Includes CATAID
environment_measures = pd.read_csv("EnvironmentMeasures.csv")  # Includes CATAID
pipe3d = pd.read_csv("pipe3d_data.csv")  # Includes CATAID, MANGAID
gema = pd.read_csv("GEMA_2.csv")  # May include MANGAID or PLATEIFU
photoobj = pd.read_csv("PhotoObj_pmqr771.csv")  # Includes objid

# Normalize 'objid' capitalization in all datasets
# For 'MagPhys' we rename 'CATAID' to 'objid'
magphys['objid'] = magphys['CATAID'].astype(str)
magphys = magphys.drop(columns=['CATAID'])

# Normalize 'objID' to 'objid' in all other datasets
datasets_to_normalize = [stellar_mass, galaxy_classified, environment_measures, photoobj]
for dataset in datasets_to_normalize:
    if 'objID' in dataset.columns:
        dataset['objid'] = dataset['objID'].astype(str)
        dataset.drop(columns=['objID'], inplace=True)

# Ensure 'objid' is the same type (string) for all datasets
core['objid'] = core['objid'].astype(str)

# Merge datasets based on objid (for SDSS-based data)
merged = core.merge(magphys, on="objid", how="left")
merged = merged.merge(stellar_mass, left_on="objid", right_on="objid", how="left")
merged = merged.merge(galaxy_classified, left_on="objid", right_on="objid", how="left")
merged = merged.merge(environment_measures, left_on="objid", right_on="objid", how="left")
merged = merged.merge(photoobj, on="objid", how="left")
merged = merged.merge(gzoo, on="objid", how="left")  # Merging with GZ_410166 data

# Merge with other identifiers (MANGAID, etc.)
merged = merged.merge(pipe3d, on="MANGAID", how="left")
merged = merged.merge(gema, on="MANGAID", how="left")

# Save the merged dataset
merged.to_csv("singularity_full_dataset.csv", index=False)

# Preview the final merged dataset
print(f"Final merged dataset shape: {merged.shape}")
print(merged[["objid", "MANGAID", "PLATEIFU", "arcsec_separation"]].head())
