    print("\nGroup Statistics:")
    print(group_stats)
else:
    print("\nNo 'group' column found. To analyze groups, add a 'group' column or bin by mass/SFR.")


# Step 3: Theory Testing
# Define a placeholder function for BSD Cosmology SFR prediction
def bsd_predicted_sfr(logmass, z):
    """
