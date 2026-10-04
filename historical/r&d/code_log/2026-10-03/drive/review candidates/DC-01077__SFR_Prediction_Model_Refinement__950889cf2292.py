from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split


# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Train the model
gb = GradientBoostingRegressor()
gb.fit(X_train, y_train)
