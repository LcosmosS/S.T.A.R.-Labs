import joblib
# After training the final model
joblib.dump(model, 'bsd_model.pkl')
# Load and test on new data
