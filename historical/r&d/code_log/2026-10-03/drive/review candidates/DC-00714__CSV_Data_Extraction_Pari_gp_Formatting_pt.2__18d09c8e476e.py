from astropy.io import fits
import pandas as pd
hdul = fits.open('pipe3d_data.fits')
data = hdul[1].data  # Assuming the first extension is a table
df = pd.DataFrame(data)
df.to_csv('pipe3d_data.csv', index=False, quoting=csv.QUOTE_ALL)
