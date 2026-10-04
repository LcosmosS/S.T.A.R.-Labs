mse_fold = mean_squared_error(y_test, y_pred_fold) mse_list.append(mse_fold) print(f"Fold {fold+1} MSE: {mse_fold:.4f}")
print(f"Average MSE: {np.mean(mse_list):.4f}")Save the modeljoblib.dump(model, 'sfr_prediction_model.joblib')is this the model as laid out for testing with python?
