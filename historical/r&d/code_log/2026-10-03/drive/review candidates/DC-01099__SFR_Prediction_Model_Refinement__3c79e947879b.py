import joblib
gb = joblib.load("/mnt/data/best_gb_model.pkl")
print("Model loaded successfully ✅")


If you renamed or reuploaded the model with a different name, replace it with the new filename shown in os.listdir().
