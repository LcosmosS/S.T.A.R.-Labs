for col in flux_columns:
    if (df_filtered[col] < 0).any():
        df_filtered = df_filtered[df_filtered[col] >= 0]
        print(f"Removed rows with negative values in {col}")


# Optional: Use QCFLAG if available for additional filtering
if 'QCFLAG' in df.columns:
    df_filtered = df_filtered[df_filtered['QCFLAG'] == 1]  # Assuming 1 indicates valid data
    print(f"Filtered dataset shape after QCFLAG: {df_filtered.shape}")


# Save the filtered dataset
df_filtered.to_csv('filtered_Pipe3D_v2.csv', index=False)
print("Filtered dataset saved to 'filtered_Pipe3D_v2.csv'")
