import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt


# Step 1: Load the dataset
df = pd.read_csv('/home/pmqr7/pipe3d_data.csv')  # Ensure to use the correct path


# Step 2: Inspect columns to confirm features (only print a subset of columns to avoid clutter)
print(df.columns)


# Step 3: Define the relevant target and features (you can modify this list based on your requirements)
target = 'log_SFR_Ha'  # Target variable (you can modify this based on your choice)
features = ['log_Mass_gas', 'log_Mass', 'log_SFR_SF', 'log_SFR_D_C', 'OH_O3N2_cen', 'log_OIII_Hb_cen']  # Example features, adjust as necessary


# Step 4: Filter out rows with missing values for the target and selected features
df_filtered = df[['CATAID', target] + features].dropna()


# Step 5: Separate features (X) and target (y)
X = df_filtered[features]
y = df_filtered[target]


# Step 6: Split the dataset into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Step 7: Initialize and train a Random Forest model
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)


# Step 8: Make predictions on the test set
y_pred = rf.predict(X_test)


# Step 9: Evaluate the model performance
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)


# Step 10: Print model performance metrics
print(f'Mean Squared Error (MSE): {mse:.4f}')
print(f'R-squared (R²): {r2:.4f}')


# Step 11: Plot Residuals (Predictions vs Actual values)
plt.figure(figsize=(8, 6))
residuals = y_test - y_pred
plt.scatter(y_pred, residuals, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted SFR')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted SFR')
plt.show()


# Step 12: Plot Feature Importances
plt.figure(figsize=(8, 6))
importances = rf.feature_importances_
sorted_idx = importances.argsort()
plt.barh([features[i] for i in sorted_idx], importances[sorted_idx])
plt.xlabel('Importance')
plt.title('Feature Importances (Random Forest)')
plt.show()
