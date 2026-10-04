from astroquery.sdss import SDSS
from astroquery.utils import table
from astropy.coordinates import SkyCoord
import astropy.units as u


# Define the region of interest (RA, DEC, and radius)
coord = SkyCoord(ra=150.116321, dec=2.2052, unit=(u.deg, u.deg), frame='icrs')
radius = 0.1 * u.deg  # 0.1 degree radius, adjust as needed


# Query SDSS for galaxies in this region
xid = SDSS.query_region(coord, radius=radius, spectro=True)


# Retrieve galaxy data (stellar mass, redshift, etc.)
galaxies = SDSS.get_spectra(plate=xid['plate'], fiberID=xid['fiberID'], mjd=xid['mjd'])


# Convert the result into a table (optional)
galaxies_table = table.Table(galaxies)


# Optionally save to CSV for later use
galaxies_table.write("sdss_galaxies.csv", format="csv")
