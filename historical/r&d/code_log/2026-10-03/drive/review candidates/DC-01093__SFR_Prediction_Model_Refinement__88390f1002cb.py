import joblib


# Save using joblib with compression to ensure compatibility
joblib.dump(gb, "best_gb_model_resaved.pkl", compress=3)
