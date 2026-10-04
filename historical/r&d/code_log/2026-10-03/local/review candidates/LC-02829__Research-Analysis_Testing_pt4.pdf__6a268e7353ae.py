            color = 'green' if rank == 3 else 'blue' if rank == 2 else 'black'
            plt.scatter(x_vals, y_vals, s=float(max(density_size, 1)), c=color, alpha=0.5, label=f'Rank {rank}')
            plt.scatter(x_vals, -y_vals, s=float(max(density_size, 1)), c=color, alpha=0.5)
            if rank > 0:
                contour_y = np.full_like(x_vals, float(5))
                plt.plot(x_vals, contour_y, 'r--', label=f'Regulator {scaled_reg:.0f}')
                plt.plot(x_vals, -contour_y, 'r--')
            plt.title(f'Curve y² = x³ + {a}x + {b}, Density: {leading_coeff * 177:.0f}')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend()
            plt.grid(True)
            plt.savefig(f"curve_{a}_{b}.png")
            plt.close()
            print(f"Polynomial plot saved as curve_{a}_{b}.png")
        except Exception as e:
            print(f"Failed to generate polynomial plot: {e}")

    print("-" * 20)
    return success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E

# Restore state from the first 10 attempts
X_data = [
    [13, 377, math.log(61540336), math.log(61540336), 1],  # Attempt 1
    [2, 144, math.log(8958464), math.log(4479232), 1],    # Attempt 2
