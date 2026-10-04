import joblib


try:
    gb = joblib.load("my_best_gb_model.pkl")
    print("Model loaded successfully!")
except Exception as e:
    print("Error loading model:", e)
