import pandas as pd
import csv
df = pd.read_csv('pipe3d_data.csv')
9. df.to_csv('pipe3d_data_fixed.csv', index=False, quoting=csv.QUOTE_ALL)
