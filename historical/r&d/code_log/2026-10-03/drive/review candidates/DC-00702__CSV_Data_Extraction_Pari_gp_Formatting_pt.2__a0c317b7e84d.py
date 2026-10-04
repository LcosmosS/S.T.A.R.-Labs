import pandas as pd
df = pd.read_csv('fits_extract_clean.csv', sep='\t')
3. df.to_csv('fits_extract_clean_comma.csv', index=False)
