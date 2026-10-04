print("GEMA_2 shape:", GEMA_2.shape)
print("mangaHIall shape:", mangaHIall.shape)
print("Merged shape:", merged_data.shape)
   * print("Final merged shape:", final_merged_data.shape)
   * Ensure the number of rows makes sense (e.g., no unexpected drops due to inner joins).
* Inspect mangaid:
   * Confirm that mangaid and MANGAID align correctly (e.g., GEMA_2['mangaid'].isin(mangaHIall['MANGAID']).mean() should be close to 1 if they match well).
