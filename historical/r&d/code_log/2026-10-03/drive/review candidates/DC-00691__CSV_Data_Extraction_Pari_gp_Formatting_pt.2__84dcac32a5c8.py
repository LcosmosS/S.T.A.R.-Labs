import pandas as pd
import csv
df = pd.read_csv('pipe3d_data.csv')  # Or reload from FITS
8. df.to_csv('pipe3d_data_fixed.csv', index=False, quoting=csv.QUOTE_ALL)
