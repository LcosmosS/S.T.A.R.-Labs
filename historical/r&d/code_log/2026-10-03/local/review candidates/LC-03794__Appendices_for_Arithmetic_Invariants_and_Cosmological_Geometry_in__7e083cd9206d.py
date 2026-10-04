smote = SMOTE(random_state=42)

X_res, y_res = smote.fit_resample(X_clf, y_clf)



# Regime split

df_gal = df[df['predicted_regime'] == 0]

df_clust = df[df['predicted_regime'] == 1]



# Models function with non-linear stacking

def run_models(X, y, regime):

    X = imputer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)

    X_test_scaled = scaler.transform(X_test)



    pysr_model = PySRRegressor(

        niterations=300,  # Increased

        binary_operators=["+", "-", "*", "/", "pow"],
