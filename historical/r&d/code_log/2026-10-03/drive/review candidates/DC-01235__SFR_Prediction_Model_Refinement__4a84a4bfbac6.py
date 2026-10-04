import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import shap


# Step 1: Load the three CSV files
df1 = pd.read_csv('GZ_410166_2.csv')
df2 = pd.read_csv('GZ_410166.csv')
df3 = pd.read_csv('GZ_gzdv1-2.csv')


# Step 2: Merge the DataFrames on the 'recno' column (keeping all rows with 'outer' join)
merged_df = pd.merge(df1, df2, on='recno', how='outer')
merged_df = pd.merge(merged_df, df3, on='recno', how='outer')


# Step 3: Fill missing values with 0 (or another value you prefer)
merged_df.fillna(0, inplace=True)


# Step 4: Select features and target
# Adjust this according to the columns in your dataset. Assuming you want to predict 'SFR'
X = merged_df[['log_Mass', 'sfr', 'redshift', 'metallicity', 'ra', 'dec']]  # Example feature columns
y = merged_df['sfr']  # Target: 'sfr' (Star Formation Rate)


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
