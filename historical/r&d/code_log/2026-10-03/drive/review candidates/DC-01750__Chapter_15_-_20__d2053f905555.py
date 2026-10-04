   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
   
   scaler = StandardScaler()
   X_train_scaled = scaler.fit_transform(X_train)
   X_test_scaled = scaler.transform(X_test)

   models = {
       "Random Forest": RandomForestRegressor(random_state=42),
       "Gradient Boosting": GradientBoostingRegressor(random_state=42),
       "XGBoost": xgb.XGBRegressor(random_state=42),
       "LightGBM": lgb.LGBMRegressor(random_state=42)
   }
   
   results = {}
   for name, model in models.items():
       model.fit(X_train_scaled, y_train)
       y_pred = model.predict(X_test_scaled)
       r2 = model.score(X_test_scaled, y_test)
       mse = np.mean((y_pred - y_test)**2)
       results[name] = {'R2': r2, 'MSE': mse}
       print(f"{name} - R²: {r2:.4f}, MSE: {mse:.4f}")

       # --- Block 4: SHAP Analysis for Feature Importance ---
       if name == "XGBoost": # Focus on the best model
           explainer = shap.Explainer(model, X_train_scaled)
           shap_values = explainer(X_test_scaled)
           
           plt.figure()
           shap.summary_plot(shap_values, X_test, feature_names=X.columns, show=False)
           plt.title(f"SHAP Summary for {name}")
           plt.tight_layout()
           plt.savefig(f"shap_summary_{name}.png")
           plt.close()

   return results

# --- Main Execution ---
if __name__ == "__main__":
   # Load and prepare data
   df = load_and_clean_data("path_to_your_galaxy_data.csv")
   df = create_symbolic_features(df)

   # Define features and target
   base_features = ['logmass', 'z', 'metallicity', 'petrorad_r', 'ellipticity']
   symbolic_features = ['cosmo_rank', 'L_cosmo_s0.5', 'L_cosmo_s1.0', 'L_cosmo_s1.5', 'L_cosmo_s2.0']
   
   # Ensure all selected features exist in the dataframe
