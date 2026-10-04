import necessary libraries
def create_features(df, high_mass_threshold, low_mass_threshold, additional_features=[]): # as above
def main(): # Load data df = pd.read_csv('Stellar_Mass2_Table_cleaned.csv')
# Check for required columns
required_columns = ['logmass', 'z', 'sfr']
for col in required_columns:
    if col not in df.columns:
        print(f"Error: Missing column {col}")
        exit(1)


# Handle missing values: impute with mean
for col in required_columns:
    df[col].fillna(df[col].mean(), inplace=True)


# If additional features are present, impute them too
additional_features = ['metallicity', 'environment']
for feat in additional_features:
    if feat in df.columns:
        df[feat].fillna(df[feat].mean(), inplace=True)


# Set up k-fold CV
k = 5
kf = KFold(n_splits=k, shuffle=True, random_state=42)


mse_list = []
for fold, (train_idx, test_idx) in enumerate(kf.split(df)):
    print(f"Fold {fold+1}")
    train_df = df.iloc[train_idx]
    test_df = df.iloc[test_idx]
    
    # Calculate thresholds from training data
    high_mass_threshold = train_df['logmass'].quantile(0.75)
    low_mass_threshold = train_df['logmass'].quantile(0.25)
    
    # Create features
    train_features = create_features(train_df, high_mass_threshold, low_mass_threshold, additional_features)
    test_features = create_features(test_df, high_mass_threshold, low_mass_threshold, additional_features)
    
    # Fit model
    model = LinearRegression()
    model.fit(train_features, train_df['sfr'])
    
    # Predict on test set
    test_pred = model.predict(test_features)
    
    # Calculate MSE
    mse = mean_squared_error(test_df['sfr'], test_pred)
    mse_list.append(mse)
    print(f"MSE for fold {fold+1}: {mse:.4f}")
    
    # Plot observed vs. predicted
    plt.scatter(test_df['sfr'], test_pred)
    plt.xlabel('Observed SFR')
    plt.ylabel('Predicted SFR')
    plt.title(f'Fold {fold+1}: Observed vs. Predicted SFR')
    plt.savefig(f'plots/fold_{fold+1}_observed_vs_predicted.png')
    plt.close()
    
    # Plot residuals vs. logmass
    residuals = test_df['sfr'] - test_pred
    plt.scatter(test_df['logmass'], residuals)
    plt.xlabel('Logmass')
    plt.ylabel('Residuals')
    plt.title(f'Fold {fold+1}: Residuals vs. Logmass')
    plt.savefig(f'plots/fold_{fold+1}_residuals_vs_logmass.png')
    plt.close()
    
    # Plot residuals vs. z
    plt.scatter(test_df['z'], residuals)
    plt.xlabel('Redshift (z)')
    plt.ylabel('Residuals')
    plt.title(f'Fold {fold+1}: Residuals vs. z')
    plt.savefig(f'plots/fold_{fold+1}_residuals_vs_z.png')
    plt.close()


# Report average MSE
average_mse = np.mean(mse_list)
print(f"Average MSE across {k} folds: {average_mse:.4f}")


# Optionally, generate overall histograms
plt.hist(df['logmass'], bins=30, color='blue', alpha=0.7)
plt.xlabel('Logmass')
plt.ylabel('Frequency')
plt.title('Overall Logmass Distribution')
plt.savefig('plots/logmass_distribution.png')
plt.close()


plt.hist(df['sfr'], bins=30, color='green', alpha=0.7)
plt.xlabel('SFR')
plt.ylabel('Frequency')
plt.title('Overall SFR Distribution')
plt.savefig('plots/sfr_distribution.png')
plt.close()


print("Script completed.")
if name == "main": import os if not os.path.exists('plots'): os.makedirs('plots') main()
