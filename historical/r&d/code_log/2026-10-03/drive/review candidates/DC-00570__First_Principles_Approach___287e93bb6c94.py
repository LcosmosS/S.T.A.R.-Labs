    print("Running Type-Aware QFT Correlation Test...")
    results = {}
    
    # Separate data into 'Simple' and 'Recursive' buckets
    simple_data = {k: v for k, v in ucf_data.items() if v[5] == 0}
    recursive_data = {k: v for k, v in ucf_data.items() if v[5] == 1}


    # Test Simple Generator data
    if simple_data:
        simple_invariants = np.array([[v[1], v[3], v[5]] for v in simple_data.values()])
        qft_simple_complexity = np.array([model_qft_by_type(inv) for inv in simple_invariants])
        ucf_simple_volumes = np.array([v[2] for v in simple_data.values()])
