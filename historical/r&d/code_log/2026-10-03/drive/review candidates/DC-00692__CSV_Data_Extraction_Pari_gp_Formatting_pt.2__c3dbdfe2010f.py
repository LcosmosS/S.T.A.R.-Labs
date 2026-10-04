import pandas as pd
df = pd.read_csv('pipe3d_data.csv', delimiter='\t')  # Adjust delimiter as needed
5. df.to_csv('pipe3d_data_comma.csv', index=False, quoting=csv.QUOTE_ALL)
