import pandas as pd
import numpy as np


# Load the results from your test run
df = pd.read_csv('sagemath_run_results.csv')


# Drop rows where the calculation was not possible
df_clean = df.dropna(subset=['scaling_constant_K'])


# Calculate the statistical summary
stats = df_clean['scaling_constant_K'].describe()


print(stats)
