from sklearn.impute import SimpleImputer


imputer = SimpleImputer(strategy='median')
* X = imputer.fit_transform(X)
* Outliers: If your dataset has extreme values, filter them out. For example, using the Interquartile Range (IQR) method:
* python
Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1
* df = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]
* Scaling: Random Forests don’t need scaling, but if you later switch to a model like linear regression, add a scaling step:
* python
from sklearn.preprocessing import StandardScaler


scaler = StandardScaler()
* X = scaler.fit_transform(X)
