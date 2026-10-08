import gzip
import shutil
import os
from astropy.io import fits
import pandas as pd

# Step 1: Define the file paths
fits_gz_file = "gz_hubble_sdss_coadd.fits.gz"  # Path to the compressed FITS file
fits_file = "gz_hubble_sdss_coadd.fits"        # Path for the decompressed FITS file
output_csv = "gz_hubble_sdss_coadd.csv"        # Path for the output CSV file

# Step 2: Decompress the .fits.gz file
if not os.path.exists(fits_file):
    print(f"Decompressing {fits_gz_file} to {fits_file}...")
    with gzip.open(fits_gz_file, 'rb') as f_in:
        with open(fits_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print("Decompression complete.")
else:
    print(f"{fits_file} already exists, skipping decompression.")

# Step 3: Read the FITS file
print(f"Reading FITS file: {fits_file}...")
with fits.open(fits_file) as hdul:
    # FITS files contain multiple HDUs; typically, the table is in HDU 1 (index 1)
    # HDU 0 is often a primary header with no data
    # Let's inspect the HDUs to find the table
    hdul.info()  # Print information about the HDUs
    
    # Assume the table is in HDU 1 (common for Galaxy Zoo data)
    table_hdu = hdul[1]  # Access the binary table HDU
    table_data = table_hdu.data  # Extract the table data

    # Step 4: Convert the FITS table to a pandas DataFrame
    print("Converting FITS table to pandas DataFrame...")
    # The table_data is a FITS_rec object; convert it to a DataFrame
    df = pd.DataFrame(table_data)

    # Step 5: Save the DataFrame to a CSV file
    print(f"Saving DataFrame to CSV: {output_csv}...")
    df.to_csv(output_csv, index=False)
    print(f"CSV file saved successfully: {output_csv}")

# Step 6: Optional - Clean up the decompressed FITS file
# Uncomment the following lines if you want to delete the decompressed FITS file
# print(f"Cleaning up: Removing {fits_file}...")
# os.remove(fits_file)
# print("Cleanup complete.")

# Step 7: Display the first few rows of the DataFrame for verification
print("\nFirst few rows of the extracted table:")
print(df.head())
print("\nColumn names:")
print(df.columns.tolist())