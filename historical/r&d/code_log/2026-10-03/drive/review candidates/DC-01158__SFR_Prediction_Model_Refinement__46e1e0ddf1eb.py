from sklearn.model_selection import cross_val_score


cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
print("CV R² Scores:", cv_scores)
print("Mean CV R²:", np.mean(cv_scores))
