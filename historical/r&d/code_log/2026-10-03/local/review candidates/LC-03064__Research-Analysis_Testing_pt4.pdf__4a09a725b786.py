        print(f"Added twisted curve to training data: {features}, label: {rank_twist}")
except Exception as e:
    print(f"Failed to compute rank of twisted curve: {e}")

print("\nFinal training data: {training_data}")
print(f"Final labels: {training_labels}")
