print(f"R² Score: {r2}")


# Cross-validation (optional)
cv_scores = cross_val_score(model, X_scaled, y, cv=5)
print(f"Cross-Validation Scores: {cv_scores}")
print(f"Mean CV Score: {cv_scores.mean()}")
