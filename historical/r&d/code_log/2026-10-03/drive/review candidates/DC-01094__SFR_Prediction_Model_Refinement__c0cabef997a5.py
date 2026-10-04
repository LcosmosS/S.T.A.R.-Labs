import joblib


# Load the Gradient Boosting model
gb = joblib.load("/mnt/data/best_gb_model.pkl")
print("Model loaded successfully!")
