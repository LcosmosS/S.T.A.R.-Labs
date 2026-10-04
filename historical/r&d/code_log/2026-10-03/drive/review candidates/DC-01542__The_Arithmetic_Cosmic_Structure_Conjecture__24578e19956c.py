X = df[['log_mass', 'metallicity', 'av', 'rank', 'regulator']]
y = df['log_sfr']
rf = RandomForestRegressor(n_estimators=500, random_state=42)
rf.fit(X, y)
print("R^2:", rf.score(X, y))
