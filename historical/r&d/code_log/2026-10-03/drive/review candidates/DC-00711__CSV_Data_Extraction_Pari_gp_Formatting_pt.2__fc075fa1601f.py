import pandas as pd
import csv


df = pd.read_csv('pipe3d_data.csv', delimiter='\t')
3. df.to_csv('pipe3d_data2.csv', index=False, quoting=csv.QUOTE_ALL)
