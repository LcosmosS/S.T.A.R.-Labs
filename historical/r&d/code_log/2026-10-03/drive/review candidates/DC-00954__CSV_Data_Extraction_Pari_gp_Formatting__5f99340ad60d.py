# Step 2: Extract logmass for Group 2 (assuming Group 2 is labeled as 1)
try:
    logmass_group2 = df[df['groups'] == 1]['logmass'].values
    print(f"Extracted {len(logmass_group2)} logmass values for Group 2.")
