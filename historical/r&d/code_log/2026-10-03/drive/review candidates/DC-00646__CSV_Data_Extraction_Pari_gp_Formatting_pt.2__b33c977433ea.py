def main():
    # Load data
    df = pd.read_csv('Stellar_Mass2_Table_cleaned.csv')
    
    # Handle missing values
    for col in required_columns:
        df[col] = df[col].fillna(df[col].mean())
    
    # Check for additional features
    additional_features = []
    if 'metallicity' in df.columns:
        additional_features.append('metallicity')
    if 'environment' in df.columns:
        additional_features.append('environment')
    
    # Define thresholds
    high_mass_threshold = df['logmass'].quantile(0.75)
    low_mass_threshold = df['logmass'].quantile(0.25)
    
    # Create features
    features = create_features(df, high_mass_threshold, low_mass_threshold, additional_features)
    
    # Cross-validation
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    mse_list = []
    for fold, (train_idx, test_idx) in enumerate(kf.split(df)):
        train_df = df.iloc[train_idx]
        test_df = df.iloc[test_idx]
        
        # Train model
        model = LinearRegression()
        model.fit(train_features, train_df['sfr'])
        
        # Predict and evaluate
        test_pred = model.predict(test_features)
        mse = mean_squared_error(test_df['sfr'], test_pred)
        mse_list.append(mse)
        
        # Plots
        plot_diagnostics(fold, test_df, test_pred, mse)
    
    # Results
    print(f"Average MSE: {np.mean(mse_list):.4f}")
    print(f"Standard Deviation of MSE: {np.std(mse_list):.4f}")
