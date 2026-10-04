import pandas as pd
df = pd.read_csv('pipe3d_data.csv', delimiter='\t')
4. df.to_csv('new_pipe3d_data.csv', index=False)
