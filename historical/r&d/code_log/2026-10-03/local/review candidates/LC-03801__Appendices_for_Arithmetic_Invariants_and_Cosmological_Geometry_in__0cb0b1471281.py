df['predicted_regime'] = clf.predict(X_clf)



# Generator Classifier

df['generator_label'] = df['otype_int']

y_gen = df['generator_label']

gen_clf = RandomForestClassifier(random_state=42)

cv_scores_gen = cross_val_score(gen_clf, X_clf, y_gen, cv=5)

print("Generator Classifier CV Mean Accuracy:", cv_scores_gen.mean())

gen_clf.fit(X_clf, y_gen)

df['predicted_type'] = gen_clf.predict(X_clf)



# Balance

smote = SMOTE(random_state=42)

X_res, y_res = smote.fit_resample(X_clf, y_clf)



# Regime split

df_gal = df[df['predicted_regime'] == 0]

df_clust = df[df['predicted_regime'] == 1]



# Models function
