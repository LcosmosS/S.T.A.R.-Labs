from sklearn.model_selection import cross_val_score
rf_cv_scores = cross_val_score(rf, X_poly, y, cv=5, scoring='r2')
* print("RF CV R²:", rf_cv_scores.mean(), "+/-", rf_cv_scores.std())
