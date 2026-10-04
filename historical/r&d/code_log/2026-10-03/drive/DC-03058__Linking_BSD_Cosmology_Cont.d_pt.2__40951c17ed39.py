from astroquery.vizier import Vizier
v = Vizier(columns=['*'], row_limit=200000)
result = v.query_constraints(catalog='J/ApJS/233/25', RAJ2000='>0', DEJ2000='>0')  # Example: GSWLC catalog
if result:
   *     result[0].write('/home/pmqr7/data/GSWLC.csv', format='csv')
