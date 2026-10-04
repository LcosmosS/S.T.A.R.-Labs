            f.write(f"{features},{label}\n")
    print("Training data saved to selmer_training_data.txt")
else:
    print(f"\nReached maximum attempts ({attempt-1}) without finding enough 3-Selmer rank >= 3 curves.
