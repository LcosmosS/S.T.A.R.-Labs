import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler


# Load the dataset (replace 'galaxy_zoo_data.csv' with your file)
df = pd.read_csv('galaxy_zoo_data.csv')


# Preprocess the data (e.g., handle missing values)
df = df.dropna()  # Drop rows with missing values
df = df[(df['log_Mass'] > 9) & (df['sfr'] > 0)]  # Filter for galaxies with mass > 9 and SFR > 0


# Select features (X) and target (y)
X = df[['log_Mass', 'sfr', 'redshift', 'metallicity', 'ra', 'dec']]  # Add more features as needed
y = df['sfr']  # Target: SFR


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Standardize the features (optional but often helpful)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Train a Random Forest model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)
