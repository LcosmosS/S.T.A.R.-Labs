import pandas as pd


# Load each dataset
df_main = pd.read_csv("filtered_dataset.csv")
df_class = pd.read_csv("GalaxiesClassified.csv")
df_mass = pd.read_csv("Stellar_Mass2_Table.csv")
df_hi = pd.read_csv("mangaHIall.csv")


# Print their column names to inspect merge keys
print("\nfiltered_dataset.csv columns:\n", df_main.columns)
print("\nGalaxiesClassified.csv columns:\n", df_class.columns)
print("\nStellar_Mass2_Table.csv columns:\n", df_mass.columns)
print("\nmangaHIall.csv columns:\n", df_hi.columns)
