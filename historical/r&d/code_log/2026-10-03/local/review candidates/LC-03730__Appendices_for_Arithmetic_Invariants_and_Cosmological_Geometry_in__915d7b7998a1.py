    print("="*60)
    print(f"Analyzing Curve: {curve_name}")
    print(f"Equation: {E}")
    print("="*60)

    results = {
        'curve_name': curve_name,
        'equation': str(E),
        'evidence': {}
    }

    # --- 1. Baseline: Standard SageMath Rank ---
    # This uses Sage's default (often PARI-based) methods for 2-descent.
    try:
        rank = E.rank()
        results['evidence']['sage_algebraic_rank'] = rank
        print(f"[Step 1] SageMath Algebraic Rank (Best Effort): {rank}")
