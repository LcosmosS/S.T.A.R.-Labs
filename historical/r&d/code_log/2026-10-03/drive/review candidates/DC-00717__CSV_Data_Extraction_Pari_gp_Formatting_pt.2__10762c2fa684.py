import pandas as pd
import csv


df = pd.read_csv('pipe3d_data.csv')
total_rows = len(df)
rows_per_file = total_rows // 3


df1 = df.iloc[0:rows_per_file]
df2 = df.iloc[rows_per_file:2*rows_per_file]
df3 = df.iloc[2*rows_per_file:]


df1.to_csv('pipe3d_data_part1.csv', index=False, quoting=csv.QUOTE_ALL)
df2.to_csv('pipe3d_data_part2.csv', index=False, quoting=csv.QUOTE_ALL)
df3.to_csv('pipe3d_data_part3.csv', index=False, quoting=csv.QUOTE_ALL)


print(f"Total rows: {total_rows}")
print(f"Rows per file: {rows_per_file}")
print(f"df1 rows: {len(df1)}")
print(f"df2 rows: {len(df2)}")
print(f"df3 rows: {len(df3)}")
