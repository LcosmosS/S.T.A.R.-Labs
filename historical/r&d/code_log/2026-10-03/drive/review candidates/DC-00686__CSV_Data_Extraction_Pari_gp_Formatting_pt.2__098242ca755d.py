import pandas as pd
df = pd.read_csv('large_file.csv', delimiter='\t')  # Replace '\t' with your delimiter
* df.to_csv('new_file.csv', index=False)
