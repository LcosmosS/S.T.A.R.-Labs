import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import shap


# Step 1: Load the CSV file
df1 = pd.read_csv('merged_output.csv', low_memory=False)


# Print columns to confirm
print("Columns in merged DataFrame:", df1.columns)


# --- Check if 'fS' (Halpha flux) exists and calculate SFR ---
if 'fS' in df1.columns:
    # Calculate SFR from Halpha flux (assuming fS is in erg/s/cm²)
    df1['SFR'] = df1['fS'] / (1.26e-41)  # SFR in solar masses per year
    print("SFR column successfully created from fS.")
else:
    print("Column 'fS' not found. Cannot calculate SFR.")


# --- Randomly select features ---
np.random.seed(42)


# Ensure 'SFR' is available as the target (we just calculated it above)
if 'SFR' in df1.columns:
    X = df1[['log_Mass', 'sfr', 'redshift', 'metallicity', 'ra', 'dec']]  # Example feature columns
    y = df1['SFR']  # Target: 'SFR' (Star Formation Rate)
else:
    print("SFR column not available for target variable.")


# Step 5: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Step 6: Standardize the features (optional but often helpful for gradient-based models)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Step 7: Train the model using Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)


# Step 8: Predict on the test set
y_pred = model.predict(X_test_scaled)


# Step 9: Evaluate the model's performance
mse = mean_squared_error(y_test, y_pred)
r2 = model.score(X_test_scaled, y_test)
