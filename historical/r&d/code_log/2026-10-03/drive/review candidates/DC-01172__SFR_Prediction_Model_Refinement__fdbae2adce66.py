import pandas as pd


# Load datasets
df_main = pd.read_csv("filtered_dataset.csv")
df_class = pd.read_csv("GalaxiesClassified.csv")
df_mass = pd.read_csv("Stellar_Mass2_Table.csv")
df_hi = pd.read_csv("mangaHIall.csv")


# Normalize all column names to lowercase
df_main.columns = df_main.columns.str.lower()
df_class.columns = df_class.columns.str.lower()
df_mass.columns = df_mass.columns.str.lower()
df_hi.columns = df_hi.columns.str.lower()


# Print column names to identify the correct merge key
print("\nMain Dataset Columns:\n", df_main.columns.tolist())
print("\nClassified Dataset Columns:\n", df_class.columns.tolist())
print("\nStellar Mass Columns:\n", df_mass.columns.tolist())
print("\nHI Dataset Columns:\n", df_hi.columns.tolist())
