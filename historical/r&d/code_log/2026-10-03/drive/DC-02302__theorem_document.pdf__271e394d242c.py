from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
X = galaxy_data[['log_mass', 'sfr_norm']]
y = galaxy_data['sfr']X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestRegressor()
model.fit(X_train, y_train)
score = model.score(X_test, y_test)
