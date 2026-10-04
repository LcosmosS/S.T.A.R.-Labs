df['regime_label'] = (df['z'] >= 0.1).astype(int)  # 0 galactic, 1 cluster

X_clf = df[['Fg', 'Fr', 'Fz', 'EBV', 'plx', 'pmRA', 'pmDE', 'flux_gr', 'flux_rz', 'log_EBV', 'pm_mag']]

y_clf = df['regime_label']

X_clf_train, X_clf_test, y_clf_train, y_clf_test = train_test_split(X_clf, y_clf, test_size=0.2,
random_state=42)

clf = RandomForestClassifier(random_state=42)

clf.fit(X_clf_train, y_clf_train)

clf_acc = clf.score(X_clf_test, y_clf_test)

print("Regime Classifier Accuracy:", clf_acc)



# Predict regimes to balance if needed

df['predicted_regime'] = clf.predict(X_clf)



# Regime split using predicted (for robustness)

df_gal = df[df['predicted_regime'] == 0]

df_clust = df[df['predicted_regime'] == 1]



imputer = SimpleImputer(strategy='mean')
