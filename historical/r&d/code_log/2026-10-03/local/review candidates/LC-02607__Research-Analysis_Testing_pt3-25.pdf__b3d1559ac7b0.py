print(f"\nCompleted: {successful_curves} successful curves analyzed out of {attempts} attempts")
if X_data:
    print("\nFinal classifier data summary:")
    print(f"Total curves analyzed: {len(X_data)}")
    print(f"Success rate: {sum(y_data) / len(y_data):.2%}")
if interweb_data:
    print("\nInterweb nodes saved to interweb_nodes.txt")
    print("Sample nodes:", interweb_data[:2])
    print("Interweb plot saved to interweb_plot.png")
    print("Rank 3 curves logged in rank3_curves.txt")
    print("Unique curves logged in unique_curves.txt")
