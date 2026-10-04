# Step 1: Explore Trends
plt.figure(figsize=(10, 5))


# Logmass vs. SFR
plt.subplot(1, 2, 1)
plt.scatter(df[logmass_col], df[sfr_col], alpha=0.5)
plt.xlabel('Log Stellar Mass')
plt.ylabel('Star Formation Rate')
plt.title('Logmass vs. SFR')


# z vs. SFR
plt.subplot(1, 2, 2)
plt.scatter(df[z_col], df[sfr_col], alpha=0.5)
plt.xlabel('Redshift (z)')
plt.ylabel('Star Formation Rate')
plt.title('z vs. SFR')


plt.tight_layout()
plt.savefig('trends_plot.png')
plt.close()
print("Saved trends plot as 'trends_plot.png'.")


# Step 2: Group Analysis
# Bin logmass into quartiles if 'group' column doesn’t exist
if 'group' not in df.columns:
    df['group'] = pd.cut(df[logmass_col], bins=4, labels=['Low', 'Mid-Low', 'Mid-High', 'High'])
    print("Created 'group' column by binning logmass into 4 quartiles.")


# Calculate group statistics
group_stats = df.groupby('group').agg({
    logmass_col: ['mean', 'median', 'std'],
    z_col: ['mean', 'median', 'std'],
