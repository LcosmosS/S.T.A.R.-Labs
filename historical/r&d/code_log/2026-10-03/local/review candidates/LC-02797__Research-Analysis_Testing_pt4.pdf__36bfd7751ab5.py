    plt.savefig("interweb_plot.png")
    plt.close()

print(f"\nCompleted: {successful_curves} successful curves analyzed out of {attempts} attempts")
if X_data:
    print(f"Total curves analyzed: {len(X_data)}")
    print(f"Success rate: {sum(y_data) / len(y_data):.2%}")
if interweb_data:
    print("Interweb nodes saved to interweb_nodes.txt")
    print("Interweb plot saved to interweb_plot.png")
