from sklearn.impute import SimpleImputer


# Impute missing values with median
imputer = SimpleImputer(strategy='median')
X = imputer.fit_transform(X)
