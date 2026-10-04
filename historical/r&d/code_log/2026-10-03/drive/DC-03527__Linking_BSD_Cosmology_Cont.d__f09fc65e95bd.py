from sklearn.model_selection import train_test_split


# Split the data (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
* X_train and y_train: Training features and target.
* X_test and y_test: Testing features and target.
* random_state=42: Ensures reproducibility.
