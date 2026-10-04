import pandas as pd
import csv
df = pd.read_csv('pipe3d_data.csv')
6. df.to_csv('pipe3d_data_fixed.csv', index=False, quoting=csv.QUOTE_ALL)
