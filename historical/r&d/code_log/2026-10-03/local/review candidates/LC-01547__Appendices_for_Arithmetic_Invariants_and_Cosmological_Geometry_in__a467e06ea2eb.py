    # Display final results in a clean table format
    results_df = pd.DataFrame(results_list)
    print("\n\n" + "="*70)
    print("                 FINAL QUERY RESULTS")
    print("="*70)
    print(results_df.to_string())
    print("\n\nExecution complete. Review the 'LMFDB Found' and 'LMFDB Label'
