            if selmer3_rank >= Integer(3):
                training_data.append(features)
                training_labels.append(selmer3_rank)
                print(f"Added twisted curve to training data: {features}, label: {selmer3_rank}")
except Exception as e:
    print(f"Failed to compute rank of twisted curve: {e}")

# Improved cosmic interweb plot with fixes for complex warnings
print("\nGenerating improved cosmic interweb plot...")
try:
    import matplotlib.pyplot as plt