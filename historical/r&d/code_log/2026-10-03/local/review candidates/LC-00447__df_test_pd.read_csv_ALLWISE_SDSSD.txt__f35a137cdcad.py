df_test = pd.read_csv("ALLWISE_SDSSDR16.csv", usecols=['RA_ICRS', 'DE_ICRS'], nrows=10000)
coords = SkyCoord(ra=df_test['RA_ICRS']*u.deg, dec=df_test['DE_ICRS']*u.deg)
center = SkyCoord(ra=185.0*u.deg, dec=32.5*u.deg)
separations = coords.separation(center).deg
print(f"Max separation: {separations.max():.2f}°, Rows outside 5°: {(separations > 5.0).sum()}")