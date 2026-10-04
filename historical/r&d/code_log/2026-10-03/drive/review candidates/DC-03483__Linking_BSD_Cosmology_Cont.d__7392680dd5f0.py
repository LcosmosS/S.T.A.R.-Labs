if missing_cols:
    print(f"Error: Missing columns: {missing_cols}")
    return


# Handle missing values without chained assignment
for col in required_columns:
    df[col] = df[col].fillna(df[col].mean())


# Check for additional features
additional_features = []
for feat in ['metallicity', 'environment']:
    if feat in df.columns:
        additional_features.append(feat)
        df[feat] = df[feat].fillna(df[feat].mean())
        print(f"Using additional feature: {feat}")


# Set model type ('linear', 'random_forest', 'gradient_boosting')
model_type = 'linear'  # Change to explore non-linear models


# Cross-validation setup
k = 5
kf = KFold(n_splits=k, shuffle=True, random_state=42)
mse_list = []


for fold, (train_idx, test_idx) in enumerate(kf.split(df)):
    print(f"\nProcessing Fold {fold+1}/{k}")
    train_df = df.iloc[train_idx]
    test_df = df.iloc[test_idx]
    
    # Define thresholds as quantiles from training data
    # Adjust quantiles (e.g., 0.8) to optimize
    high_mass_threshold = train_df['logmass'].quantile(0.75)
    low_mass_threshold = train_df['logmass'].quantile(0.25)
    
    # Create features
    train_features = create_features(train_df, high_mass_threshold, low_mass_threshold, additional_features)
    test_features = create_features(test_df, high_mass_threshold, low_mass_threshold, additional_features)
    
    # Get model
    model = get_model(model_type)
    
    # Train model
    model.fit(train_features, train_df['sfr'])
    
    # Predict and evaluate
    test_pred = model.predict(test_features)
    mse = mean_squared_error(test_df['sfr'], test_pred)
    mse_list.append(mse)
    print(f"Fold {fold+1} MSE: {mse:.4f}")
    
    # Generate diagnostic plots
    plot_diagnostics(fold, test_df, test_pred, mse)


# Report cross-validation results
avg_mse = np.mean(mse_list)
std_mse = np.std(mse_list)
print(f"\nCross-Validation Results:")
print(f"Average MSE: {avg_mse:.4f}")
print(f"Standard Deviation of MSE: {std_mse:.4f}")
print("Plots saved in 'plots/' directory.")
print("Script completed successfully!")
if __name__ == "__main__": main()
