print(f"NaNs in target: {np.isnan(y_train).sum()}")
print(f"Shape before cleaning: {X_train_scaled.shape}, {y_train.shape}")
print(f"Shape after cleaning: {X_train_scaled_clean.shape}, {y_train_clean.shape}")
