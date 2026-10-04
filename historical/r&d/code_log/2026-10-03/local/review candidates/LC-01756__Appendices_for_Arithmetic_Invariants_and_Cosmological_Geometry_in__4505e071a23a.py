df_list = []

for chunk in pd.read_csv("1760769987443A.csv", chunksize=chunksize):

    processed = process_chunk(chunk)

    if not processed.empty:

        df_list.append(processed)

df = pd.concat(df_list, ignore_index=True)

print("Full Data Info:", df.info())



imputer = SimpleImputer(strategy='mean')



# Regime Classifier

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