import pandas as pd
import numpy as np


# Example: Replace missing indicators
df.replace(-9999, np.nan, inplace=True)


# Apply median imputation
from sklearn.impute import SimpleImputer
imp_cols = ['OH_Mar13_N2_Re_fit', 'Av_gas_Re']
imputer = SimpleImputer(strategy='median')
df[imp_cols] = imputer.fit_transform(df[imp_cols])
