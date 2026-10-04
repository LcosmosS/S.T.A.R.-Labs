# Cross-validation setup
k = 5
kf = KFold(n_splits=k, shuffle=True, random_state=42)
mse_list = []


for fold, (train_idx, test_idx) in enumerate(kf.split(df)):
    train_df = df.iloc[train_idx]
    test_df = df.iloc[test_idx]
    
    # Train a simple linear model (or replace with your model)
    model = LinearRegression()
    model.fit(train_df[['logmass', 'z']], train_df['sfr'])
    
    # Predict and evaluate
    test_pred = model.predict(test_df[['logmass', 'z']])
    mse = mean_squared_error(test_df['sfr'], test_pred)
    mse_list.append(mse)
    print(f"Fold {fold+1} MSE: {mse:.4f}")


# Report results
avg_mse = np.mean(mse_list)
std_mse = np.std(mse_list)
print(f"\nAverage MSE: {avg_mse:.4f}")
print(f"Standard Deviation of MSE: {std_mse:.4f}")
