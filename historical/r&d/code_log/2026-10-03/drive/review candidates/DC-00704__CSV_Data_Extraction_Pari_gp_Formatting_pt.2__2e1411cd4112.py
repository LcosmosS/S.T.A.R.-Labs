import pandas as pd
df = pd.read_csv('pipe3d_data.txt', delimiter='\t')
3. df.to_csv('pipe3d_data.csv', index=False, quoting=csv.QUOTE_ALL)
