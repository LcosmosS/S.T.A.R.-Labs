# Load cleaned dataset
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score


df = pd.read_csv('cleaned_pipe3d_sfr_model.csv')
X = df[core_features]
y = df[target]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = GradientBoostingRegressor()
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
print("R² Score:", r2_score(y_test, y_pred))
