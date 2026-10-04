import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib


# Step 1: Load the filtered dataset
df = pd.read_csv('Filtered_Pipe3D.csv')
print(f"Dataset loaded with {len(df)} rows and {len(df.columns)} columns.")


# Step 2: Define the target variable and features
# Assuming 'log_SFR_Ha' is the target variable; adjust if different
X = df.drop(columns=['log_SFR_Ha'])  # Features (all columns except the target)
y = df['log_SFR_Ha']                 # Target (log_SFR_Ha)


# Step 3: Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape[0]} rows, {X_train.shape[1]} columns")
print(f"Testing set: {X_test.shape[0]} rows, {X_test.shape[1]} columns")


# Step 4: Initialize and train the Random Forest model with default settings
rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train, y_train)


# Step 5: Make predictions on the testing set
y_pred = rf_model.predict(X_test)


# Step 6: Evaluate the model's performance
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"R-squared: {r2:.4f}")


# Optional Step 7: Hyperparameter tuning using GridSearchCV
# Define a grid of hyperparameters to search
param_grid = {
    'n_estimators': [100, 200, 300],      # Number of trees
    'max_depth': [10, 20, None],          # Maximum depth of trees
    'min_samples_split': [2, 5, 10]       # Minimum samples required to split a node
}


# Initialize GridSearchCV with 5-fold cross-validation
grid_search = GridSearchCV(estimator=RandomForestRegressor(random_state=42),
                           param_grid=param_grid,
                           cv=5,
                           scoring='neg_mean_squared_error',
                           n_jobs=-1)  # Use all available cores


# Fit the grid search to the training data
grid_search.fit(X_train, y_train)


# Get the best model from the grid search
best_rf_model = grid_search.best_estimator_


# Evaluate the tuned model on the testing set
y_pred_tuned = best_rf_model.predict(X_test)
mse_tuned = mean_squared_error(y_test, y_pred_tuned)
r2_tuned = r2_score(y_test, y_pred_tuned)
print(f"Tuned Mean Squared Error (MSE): {mse_tuned:.4f}")
print(f"Tuned R-squared: {r2_tuned:.4f}")


# Optional Step 8: Feature Importance Analysis
# Get feature importances from the best model
importances = best_rf_model.feature_importances_
feature_names = X_train.columns
feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
print("\nFeature Importances (Top 5):")
print(feature_importance_df.head())


# Save the feature importance dataframe to a CSV for further analysis
feature_importance_df.to_csv('feature_importances.csv', index=False)
print("Feature importances saved to 'feature_importances.csv'")


# Optional Step 9: Save the best model for future use
joblib.dump(best_rf_model, 'best_rf_model.pkl')
print("Best model saved to 'best_rf_model.pkl'")
