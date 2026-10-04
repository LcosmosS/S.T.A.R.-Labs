from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='median') X = imputer.fit_transform(X)
