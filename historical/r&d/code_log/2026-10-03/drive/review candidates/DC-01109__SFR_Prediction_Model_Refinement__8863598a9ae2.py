import joblib


# Use full path from your WSL Linux environment
gb = joblib.load("/home/pmqr7/best_gb_model.pkl")
print("Model loaded successfully!")
