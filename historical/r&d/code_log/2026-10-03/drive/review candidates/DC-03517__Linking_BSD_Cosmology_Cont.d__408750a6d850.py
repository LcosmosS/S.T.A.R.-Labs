import joblib


# After training the final model
joblib.dump(model, 'bsd_model.pkl')


# Load and test on new data
new_df = pd.read_csv('new_dataset.csv')
for col in required_columns + optional_columns:
    if col in new_df.columns:
        new_df[col] = new_df[col].fillna(new_df[col].mean())
    else:
        new_df[col] = 0
if 'ra' in new_df.columns and 'dec' in new_df.columns:
    new_df['environment'] = new_df.groupby(['ra', 'dec'])['ra'].transform('size')
else:
    new_df['environment'] = 0


X_new = np.array([predict_sfr_features(row, l_1, order) for _, row in new_df.iterrows()])
y_new = new_df['sfr'].values
loaded_model = joblib.load('bsd_model.pkl')
y_new_pred = loaded_model.predict(X_new)
new_mse = mean_squared_error(y_new, y_new_pred)
* print(f"MSE on new dataset: {new_mse:.4f}")
