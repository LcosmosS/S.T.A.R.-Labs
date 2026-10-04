            texts.append(text)
    adjust_text(texts, ax=ax, arrowprops=dict(arrowstyle='-', color='gray'))
    ax.set_xlabel('Log(Discriminant)')
    ax.set_ylabel('Log(Conductor)')
    ax.set_zlabel('Rank')
    ax.set_title('Cosmic Interweb: Nodes and Weighted Filaments (Improved)')

    ax.grid(True)
    plt.savefig("interweb_improved.png")
    plt.close()
    print("Improved cosmic interweb plot saved as interweb_improved.png")
except Exception as e:

    print(f"Failed to generate improved interweb plot: {e}")

print(f"\nFinal training data: {training_data}")
print(f"Final labels: {training_labels}")
