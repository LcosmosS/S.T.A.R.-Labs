    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25,
random_state=42)

    print(f"  - Data split into {len(X_train)} training samples and {len(X_test)} test
