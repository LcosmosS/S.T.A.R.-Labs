    plt.text(0.05, 0.95, results_text, transform=plt.gca().transAxes, fontsize=12,
             verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', fc='wheat', alpha=0.5))
             
    plt.savefig(f"{OUTPUT_PLOT_PREFIX}_log_log_regression.png")
    plt.close()
    print("  - Final plot saved.")


if __name__ == "__main__":
    main()
