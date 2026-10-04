import pandas as pd
import numpy as np

print("Starting Merge 1...")
left_df = pd.read_csv("ALLWISE_SDSSDR16.csv", low_memory=False)
left_df = left_df.rename(columns={"RA_ICRS": "ra", "DE_ICRS": "dec"})
print(f"Rows in ALLWISE_SDSSDR16.csv: {len(left_df)}, Columns: {len(left_df.columns)}")

right_df = pd.read_csv("TwoMass_SDSSDR16.csv", low_memory=False)
right_df = right_df.rename(columns={"RA_ICRS": "ra", "DE_ICRS": "dec"})
print(f"Rows in TwoMass_SDSSDR16.csv: {len(right_df)}, Columns: {len(right_df.columns)}")

merged_df = left_df.merge(right_df, on=['ra', 'dec'], how='left', suffixes=('', '_dup'))
dup_cols = [col for col in merged_df.columns if '_dup' in col]
merged_df = merged_df.drop(columns=dup_cols)
merged_df = merged_df.drop_duplicates(subset=['ra', 'dec'], keep='first')
print(f"Rows after merging and deduplication: {len(merged_df)}")

merged_df.to_csv("merge_1.csv", index=False)
print("Saved to merge_1.csv")