import joblib


model_path = "/home/idies/workspace/Temporary/pmqr771/scratch/PKL/astype_copy.pkl"


try:
    gb = joblib.load(model_path)
    print("✅ Model loaded successfully!")
except Exception as e:
    print("❌ Failed to load model:", e)
