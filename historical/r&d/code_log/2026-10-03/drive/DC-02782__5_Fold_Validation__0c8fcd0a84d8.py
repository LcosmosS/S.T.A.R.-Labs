model.fit(X_train, y_train) # Refit
y_pred_fold = [] for _, galaxy in X_test.iterrows(): y_pred_fold.append(predict_sfr(galaxy, L_1, rank)) y_pred_fold = np.array(y_pred_fold)
mse_fold = mean_squared_error(y_test, y_pred_fold) mse_list.append(mse_fold) print(f"Fold {fold+1} MSE: {mse_fold:.4f}")
print(f"Average MSE: {np.mean(mse_list):.4f}")Save the modeljoblib.dump(model, 'sfr_prediction_model.joblib')is this the model as laid out for testing with python?
