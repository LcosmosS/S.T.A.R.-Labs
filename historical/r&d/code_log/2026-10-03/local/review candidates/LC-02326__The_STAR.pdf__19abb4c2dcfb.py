        print(f"R^2 Score (CatBoost, Test): {r2_cat:.4f}")

# Blend symbolic regression with HistGradientBoosting
========================================================================
============================================================
y_pred_blend = (y_pred_hgb + y_pred_symbolic) / 2
r2_blend = r2_score(y_test, y_pred_blend)
print(f"R^2 Score (Blended HGB + Symbolic, Test): {r2_blend:.4f}")
y_pred_all = (hgb.predict(X_train_scaled) + symbolic_reg.predict(X_train_scaled)) / 2
percentiles = np.percentile(y_pred_all - y_train, [5, 95])
print(f"Blended Model 90% Prediction Interval: [{percentiles[0]:.4f}, {percentiles[1]:.4f}]")

# Plot blended predictions vs actual
========================================================================
========================================================================
=====
plt.scatter(y_test, y_pred_blend, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel("Actual log_SFR_Ha_raw")
plt.ylabel("Predicted log_SFR_Ha_raw (Blended HGB + Symbolic)")
plt.title("Blended Model: Actual vs Predicted")
plt.savefig("blended_actual_vs_pred.png", dpi=150)
plt.close()

# SHAP Analysis
========================================================================
========================================================================
==========================
sample_idx = np.random.choice(X_test_scaled.shape[0], min(1000, X_test_scaled.shape[0]),
replace=False)
X_test_scaled_sample = X_test_scaled[sample_idx]
