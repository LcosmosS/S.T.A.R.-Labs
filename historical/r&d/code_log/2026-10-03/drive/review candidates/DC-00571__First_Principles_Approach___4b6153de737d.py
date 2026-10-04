        corr, p_val = pearsonr(ucf_simple_volumes, qft_simple_complexity)
        results['Simple_Type'] = {'correlation': corr, 'p_value': p_val}
        print(f"  > Simple Type Correlation (Volume vs QFT): {corr:.4f} (p={p_val:.4f})")
    
    # Test Recursive Generator data
    if recursive_data:
        recursive_invariants = np.array([[v[1], v[3], v[5]] for v in recursive_data.values()])
        qft_recursive_complexity = np.array([model_qft_by_type(inv) for inv in recursive_invariants])
        ucf_recursive_volumes = np.array([v[2] for v in recursive_data.values()])
