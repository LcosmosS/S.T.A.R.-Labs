import joblib


# Save models
joblib.dump(gb, 'gradient_boosting_model.pkl')
joblib.dump(rf, 'random_forest_model.pkl')
