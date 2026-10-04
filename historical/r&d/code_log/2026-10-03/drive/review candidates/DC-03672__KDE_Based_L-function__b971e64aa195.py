import pandas as pd
import numpy as np


# Load the dataset
df = pd.read_csv("GZ_gzdv1-2.csv", low_memory=False)


# Replace inf/-inf with NaN
df.replace([np.inf, -np.inf], np.nan, inplace=True)


# Drop all rows with any NaN values
df_cleaned = df.dropna()


# Save to a new CSV file
df_cleaned.to_csv("GZ_gzdv1-2_cleaned.csv", index=False)


print(f"Original shape: {df.shape}")
print(f"Cleaned shape: {df_cleaned.shape}")
print("Cleaned data saved to GZ_gzdv1-2_cleaned.csv")
