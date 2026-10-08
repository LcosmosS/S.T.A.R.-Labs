import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score

# --- 1. Data Loading and Merging ---
# Load the datasets
GEMA_2 = pd.read_csv('GEMA_2.csv')
pipe3d_data2 = pd.read_csv('pipe3d_data2.csv')
mangaHIall = pd.read_csv('mangaHIall.csv')

# Merge GEMA_2 with mangaHIall using left_on and right_on
merged_data = pd.merge(GEMA_2, mangaHIall, left_on='mangaid', right_on='MANGAID', how='inner')

# Drop the redundant 'MANGAID' column
merged_data = merged_data.drop(columns=['MANGAID'])

# Merge with pipe3d_data2 using 'mangaid'
final_merged_data = pd.merge(merged_data, pipe3d_data2, on='mangaid', how='inner')

# --- 2. Data Preparation ---
# Define target and features
target = 'log_SFR_Ha'
base_features = ['log_Mass_gas', 'nsa_mstar', 'log_Mass', 'V-band_SB_at_Re', 
                 'vel_sigma_Re', 'OH_Mar13_N2_Re_fit', 'Av_gas_Re']

# Impute missing values with median
imputer = SimpleImputer(strategy='median')
final_merged_data[base_features] = imputer.fit_transform(final_merged_data[base_features])

# Drop rows with missing target
final_merged_data = final_merged_data.dropna(subset=[target])
y = final_merged_data[target]
X = final_merged_data[base_features]

# --- 3. Feature Engineering ---
# Add interaction and nonlinear terms
final_merged_data['log_Mass_gas_times_nsa_mstar'] = final_merged_data['log_Mass_gas'] * final_merged_data['nsa_mstar']
final_merged_data['log_Mass_gas_times_metallicity'] = final_merged_data['log_Mass_gas'] * final_merged_data['OH_Mar13_N2_Re_fit']
final_merged_data['log_Mass_gas_squared'] = final_merged_data['log_Mass_gas'] ** 2

# Generate polynomial features
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)
feature_names = poly.get_feature_names_out(base_features)

# --- 4. Model Training and Evaluation ---
# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)

# Initialize and train Random Forest
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)
print(f"Random Forest - Test MSE: {mse_rf:.4f}, R-squared: {r2_rf:.4f}")

# Initialize and train Gradient Boosting
gb = GradientBoostingRegressor(random_state=42)
gb.fit(X_train, y_train)
y_pred_gb = gb.predict(X_test)
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)
print(f"Gradient Boosting - Test MSE: {mse_gb:.4f}, R-squared: {r2_gb:.4f}")