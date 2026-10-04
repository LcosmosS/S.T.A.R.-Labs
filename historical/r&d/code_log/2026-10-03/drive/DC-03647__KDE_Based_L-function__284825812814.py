import pandas as pd
import numpy as np


# Load the cleaned data
gz_df = pd.read_csv('/mnt/data/GZ_gzdv1-2_cleaned.csv')


# Select only numeric columns
numeric_df = gz_df.select_dtypes(include=[np.number])


# Check for infinities in numeric columns only
print("Any NaNs:", gz_df.isna().any().any())
print("Any infs:", np.isinf(numeric_df.values).any())


This will safely bypass columns like 'objID', 'morphology', or any strings that can’t be processed with np.isinf().
