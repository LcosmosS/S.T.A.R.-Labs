import joblib


# If the file is in the same folder as your notebook
gb = joblib.load("best_gb_model.pkl")
print("Model loaded successfully!")
