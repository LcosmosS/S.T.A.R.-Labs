import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler


# Load the data (replace 'galaxy_zoo_data.csv' with your file)
df = pd.read_csv('galaxy_zoo_data.csv')


# Preprocessing: Handle missing values and filter data
df = df.dropna()  # Drop rows with missing values
df = df[(df['log_Mass'] > 9) & (df['sfr'] > 0)]  # Filter galaxies with stellar mass > 9 and SFR > 0


# Feature selection (X) and target (y)
X = df[['log_Mass', 'sfr', 'redshift', 'metallicity']]  # Features
y = df['sfr']  # Target variable (SFR)


# Scaling features if necessary
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)


# Train a Random Forest model
model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)


# Predict on the test set
y_pred = model.predict(X_test)


# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = model.score(X_test, y_test)
