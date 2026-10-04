        return None

# Main loop to test the single data-driven KAPPA
successful_results = []
for name, data in cluster_data.items():
    result = test_cluster_with_kappa(name, data['r'], data['rho'], DATA_DRIVEN_KAPPA)
    if result:
        successful_results.append(result)

# Final Summary
# =========================================
print("\n\n--- Unified Framework Test Complete ---")
if successful_results:
    df = pd.DataFrame(successful_results)
    print("Summary of clusters that successfully produced a Rank 1 curve with the
