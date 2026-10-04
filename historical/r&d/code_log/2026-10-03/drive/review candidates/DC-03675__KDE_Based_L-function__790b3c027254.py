import pandas as pd
import numpy as np


# Load cleaned dataset
gz_df = pd.read_csv('/mnt/data/GZ_gzdv1-2_cleaned.csv')


# Check for any NaN or infinite values
print("Any NaNs:", gz_df.isna().any().any())
print("Any infs:", np.isinf(gz_df.values).any())


# Describe the target variable
print(gz_df['expected_SFR'].describe())


# Optional: visualize the distribution of the target
import matplotlib.pyplot as plt
import seaborn as sns


plt.figure(figsize=(8, 4))
sns.histplot(gz_df['expected_SFR'], bins=50, kde=True)
plt.title('Distribution of expected_SFR')
plt.xlabel('expected_SFR')
plt.show()
