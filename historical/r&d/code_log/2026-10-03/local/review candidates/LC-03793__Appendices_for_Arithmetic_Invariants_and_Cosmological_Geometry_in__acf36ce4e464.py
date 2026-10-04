df['regime_label'] = (df['z'] >= 0.1).astype(int)

X_clf_cols = ['Fg', 'Fr', 'Fz', 'EBV', 'plx', 'pmRA', 'pmDE', 'flux_gr', 'flux_rz', 'log_EBV', 'pm_mag',
'coeff_sum', 'chi_ratio', 'tsnr_ratio_elg_lrg', 'morph_int', 'otype_int']

X_clf = df[X_clf_cols]

X_clf = imputer.fit_transform(X_clf)

y_clf = df['regime_label']

clf = RandomForestClassifier(random_state=42)

cv_scores = cross_val_score(clf, X_clf, y_clf, cv=5)

print("Regime Classifier CV Mean Accuracy:", cv_scores.mean())

clf.fit(X_clf, y_clf)

df['predicted_regime'] = clf.predict(X_clf)



# Generator Classifier (using otype_int/morph_int)

df['generator_label'] = df['otype_int']  # Real proxy

y_gen = df['generator_label']

gen_clf = RandomForestClassifier(random_state=42)

cv_scores_gen = cross_val_score(gen_clf, X_clf, y_gen, cv=5)

print("Generator Classifier CV Mean Accuracy:", cv_scores_gen.mean())

gen_clf.fit(X_clf, y_gen)

df['predicted_type'] = gen_clf.predict(X_clf)
