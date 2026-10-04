df_external = pd.read_csv('external_data.csv')
df_external[base_features] = imputer.transform(df_external[base_features])
X_external = poly.transform(df_external[base_features])
y_external = df_external['log_SFR_Ha']
y_external_pred = best_model.predict(X_external)
mse_external = mean_squared_error(y_external, y_external_pred)
r2_external = r2_score(y_external, y_external_pred)
print(f"External MSE: {mse_external:.4f}, R-squared: {r2_external:.4f}")
