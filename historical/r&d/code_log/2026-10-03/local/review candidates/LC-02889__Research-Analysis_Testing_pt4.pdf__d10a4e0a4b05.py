            plt.legend()
            plt.grid(True)
            plt.savefig(f"curve_{a}_{b}.png")
            plt.close()
            print(f"Polynomial plot saved as curve_{a}_{b}.png")
        except Exception as e:
            print(f"Failed to generate polynomial plot: {e}")

    print("-" * 20)
    return success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E

# Restore state from attempts 1–17
X_data = [
    [13, 377, math.log(61540336), math.log(61540336), 1],  # Attempt 1
    [2, 144, math.log(8958464), math.log(4479232), 1],    # Attempt 2
