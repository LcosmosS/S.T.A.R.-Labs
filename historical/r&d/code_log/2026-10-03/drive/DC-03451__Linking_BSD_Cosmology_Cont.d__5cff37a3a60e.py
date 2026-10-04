# Check required columns
required_columns = ['logmass', 'z', 'sfr']
missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    print(f"Error: Missing columns: {missing_cols}")
    return


# Impute missing values with mean
for col in required_columns:
    df[col].fillna(df[col].mean(), inplace=True)


# Define additional features to explore
additional_features = ['metallicity', 'environment']
for feat in additional_features:
    if feat in df.columns:
        df[feat].fillna(df[feat].mean(), inplace=True)
        print(f"Using additional feature: {feat}")


# Initial histograms for data exploration
plt.hist(df['logmass'], bins=30, color='blue', alpha=0.7)
plt.xlabel('Logmass')
plt.ylabel('Frequency')
plt.title('Logmass Distribution')
plt.savefig('plots/logmass_distribution.png')
plt.close()


plt.hist(df['sfr'], bins=30, color='green', alpha=0.7)
plt.xlabel('SFR')
plt.ylabel('Frequency')
plt.title('SFR Distribution')
plt.savefig('plots/sfr_distribution.png')
plt.close()


# 5-fold cross-validation
k = 5
kf = KFold(n_splits=k, shuffle=True, random_state=42)
mse_list = []


for fold, (train_idx, test_idx) in enumerate(kf.split(df)):
    print(f"\nProcessing Fold {fold+1}/{k}")
    train_df = df.iloc[train_idx]
    test_df = df.iloc[test_idx]
    
    # Calculate mass thresholds from training data
    high_mass_threshold = train_df['logmass'].quantile(0.75)  # Top 25% for quenching
    low_mass_threshold = train_df['logmass'].quantile(0.25)   # Bottom 25% for scaling
    
    # Generate features
    train_features = create_features(train_df, high_mass_threshold, low_mass_threshold, additional_features)
    test_features = create_features(test_df, high_mass_threshold, low_mass_threshold, additional_features)
    
    # Train model
    model = LinearRegression()
    model.fit(train_features, train_df['sfr'])
    
    # Predict and evaluate
    test_pred = model.predict(test_features)
    mse = mean_squared_error(test_df['sfr'], test_pred)
    mse_list.append(mse)
    print(f"Fold {fold+1} MSE: {mse:.4f}")
    
    # Generate diagnostic plots
    plot_diagnostics(fold, test_df, test_pred, mse)


# Report results
avg_mse = np.mean(mse_list)
std_mse = np.std(mse_list)
print(f"\nCross-Validation Results:")
print(f"Average MSE: {avg_mse:.4f}")
print(f"Standard Deviation of MSE: {std_mse:.4f}")
print("Plots saved in 'plots/' directory.")
print("Script completed successfully!")
if __name__ == "__main__": main()
