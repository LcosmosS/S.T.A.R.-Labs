import pandas as pd import numpy as np
# Load your data (adjust path as needed)
df = pd.read_csv('your_data.csv') # Replace with your data source df = df[df['logmass'] > 0] # Filter out non-positive values print(f"Number of valid rows after filtering: {len(df)}")
