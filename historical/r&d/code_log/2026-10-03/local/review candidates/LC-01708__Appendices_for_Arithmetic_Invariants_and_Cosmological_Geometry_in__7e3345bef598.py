        plt.title('t-SNE of Galaxy Features with Cohomology and Entropy Gradient')
        plt.savefig(f'{OUTPUT_PLOT_PREFIX}_tsne_scatter_cohomology.png')
        plt.close()

    # Interactive widget
    @widgets.interact(feature=feature_cols)
    def plot_histogram(feature):
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x=feature, hue='generator_type', bins=50)
        plt.title(f'Distribution of {feature} by Generator Type')
        plt.savefig(f'{OUTPUT_PLOT_PREFIX}_histogram_{feature}.png')
        plt.show()

# --- 19. Shape Analysis ---
def analyze_noise_points(df, feature_cols):
    log_function("analyze_noise_points")
    recursive_df = df[df['generator_type'] == 'Recursive']
    noise_df = recursive_df[recursive_df['structure_cluster'] == -1]
    clustered_df = recursive_df[recursive_df['structure_cluster'] != -1]

    noise_stats = noise_df[feature_cols].describe()
    clustered_stats = clustered_df[feature_cols].describe()
    noise_nan_prop = noise_df[feature_cols].isna().mean()
    clustered_nan_prop = clustered_df[feature_cols].isna().mean()
    noise_structure_dist = noise_df['generator_structure'].apply(lambda x:
