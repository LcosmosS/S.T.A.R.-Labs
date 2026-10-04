# --- Split Data into Training and Testing Sets ---
print("Splitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Print the first 5 rows of training and testing sets
print("\nFirst 5 rows of the training set (X_train):")
print(X_train.head())


print("\nFirst 5 rows of the testing set (X_test):")
print(X_test.head())


print("\nFirst 5 rows of the target training set (y_train):")
print(y_train.head())


print("\nFirst 5 rows of the target testing set (y_test):")
print(y_test.head())
