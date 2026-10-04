print(f"Samp1e data: \n{df[key_columns] -head() if not missing_cols else df.head()}")
# Downcast numeric coLumns to save memory
def downcast_df(df) :
