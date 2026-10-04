    if additional_features is None:
        additional_features = []
    
    logmass = df['logmass']
    z = df['z']
    features = pd.DataFrame({
        'logmass': logmass,
        'z': z,
        'logmass2': logmass**2,  # Non-linear term
        'z2': z**2,              # Non-linear term
        'logmass_z': logmass * z,  # Interaction term
        'quenching': np.maximum(logmass - high_mass_threshold, 0),  # Quenching for high-mass
        'low_mass': (logmass < low_mass_threshold) * logmass  # Scaling for low-mass
    })
    
    # Include additional features if present
    for feat in additional_features:
        if feat in df.columns:
            features[feat] = df[feat]
    
    return features


def plot_diagnostics(fold, test_df, test_pred, mse):
    """Generate diagnostic plots for each fold."""
    # Observed vs. Predicted SFR
    plt.scatter(test_df['sfr'], test_pred, alpha=0.5)
    plt.plot([-5, 2], [-5, 2], 'r--')  # 1:1 line
    plt.xlabel('Observed SFR')
    plt.ylabel('Predicted SFR')
    plt.title(f'Fold {fold+1}: Observed vs. Predicted SFR (MSE: {mse:.4f})')
    plt.savefig(f'plots/fold_{fold+1}_observed_vs_predicted.png')
    plt.close()
    
    # Residuals vs. Logmass
    residuals = test_df['sfr'] - test_pred
    plt.scatter(test_df['logmass'], residuals, alpha=0.5)
    plt.axhline(0, color='r', linestyle='--')
    plt.xlabel('Logmass')
    plt.ylabel('Residuals (Observed - Predicted)')
    plt.title(f'Fold {fold+1}: Residuals vs. Logmass')
    plt.savefig(f'plots/fold_{fold+1}_residuals_vs_logmass.png')
    plt.close()
    
    # Residuals vs. Redshift (z)
    plt.scatter(test_df['z'], residuals, alpha=0.5)
    plt.axhline(0, color='r', linestyle='--')
    plt.xlabel('Redshift (z)')
    plt.ylabel('Residuals (Observed - Predicted)')
    plt.title(f'Fold {fold+1}: Residuals vs. z')
    plt.savefig(f'plots/fold_{fold+1}_residuals_vs_z.png')
    plt.close()


def main():
    # Load dataset
    csv_file = 'Stellar_Mass2_Table_cleaned.csv'
    try:
        df = pd.read_csv(csv_file)
        print(f"Loaded '{csv_file}' successfully.")
    except FileNotFoundError:
        print(f"Error: '{csv_file}' not found.")
