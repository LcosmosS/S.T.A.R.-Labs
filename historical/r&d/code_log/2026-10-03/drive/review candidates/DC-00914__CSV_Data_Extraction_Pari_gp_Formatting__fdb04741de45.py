from sklearn.impute import SimpleImputer


imputer = SimpleImputer(strategy='mean')
logmass_imputed = imputer.fit_transform(df[['logmass']])
