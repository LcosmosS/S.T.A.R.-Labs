from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import joblib


# Load your dataset (adjust based on what you're using)
import pandas as pd
data = pd.read_csv("merged_final_dataset.csv")


# Define features and target (replace 'SFR' with your target column)
X = data.drop(columns=["SFR"])
y = data["SFR"]


# Train/test split
X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)


# Train model
gb = GradientBoostingRegressor()
gb.fit(X_train, y)


# Save model and test set
joblib.dump(gb, "best_gb_model.pkl")
joblib.dump(X_test, "X_test.pkl")
