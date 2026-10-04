if X_data:
print("\nFinal classifier data summary:")
print(f"Total curves analyzed: {len(X_data)}")
print(f"Success rate: {sum(y_data) / len(y_data):.2%}")
