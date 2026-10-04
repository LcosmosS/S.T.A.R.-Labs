import pandas as pd
df = pd.read_csv('sagemath_run_results.csv')
print(df.head())
print(df['scaling_constant_K'].describe())
