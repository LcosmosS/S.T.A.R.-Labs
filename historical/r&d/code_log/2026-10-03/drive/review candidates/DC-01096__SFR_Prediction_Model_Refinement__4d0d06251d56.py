import joblib
gb = joblib.load("/mnt/data/best_gb_model.pkl")
print("Model loaded successfully!")


Let me know what os.listdir("/mnt/data") shows — if the file is missing, we’ll reupload it or set the correct path.
