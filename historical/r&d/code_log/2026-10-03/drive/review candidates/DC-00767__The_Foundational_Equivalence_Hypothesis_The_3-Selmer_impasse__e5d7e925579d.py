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
    except Exception as e:
        print(f"[Step 1] SageMath Rank computation failed: {e}")
        results['evidence']['sage_algebraic_rank'] = 'Error'


    # --- 2. PARI/GP Backend: 2-Selmer Rank ---
    # The 2-Selmer rank is a robust upper bound for the true rank.
    try:
        # Use the PARI interface directly for a robust check
        pari_E = pari(E)
        selmer_2_rank = pari_E.ellrank()[1] # ellrank() returns [rank, 2-Selmer rank, ...]
        results['evidence']['pari_2_selmer_rank'] = int(selmer_2_rank)
        print(f"[Step 2] PARI/GP 2-Selmer Rank (Upper Bound): {selmer_2_rank}")
    except Exception as e:
        print(f"[Step 2] PARI/GP 2-Selmer computation failed: {e}")
        results['evidence']['pari_2_selmer_rank'] = 'Error'


    # --- 3. PARI/GP Backend: Analytic Rank (via BSD Conjecture) ---
    # The analytic rank should equal the algebraic rank if BSD holds.
    try:
        analytic_rank_info = pari(E).ellanalyticrank()
        analytic_rank = int(analytic_rank_info[0])
        results['evidence']['pari_analytic_rank'] = analytic_rank
        print(f"[Step 3] PARI/GP Analytic Rank (via BSD): {analytic_rank}")
    except Exception as e:
        print(f"[Step 3] PARI/GP Analytic Rank computation failed: {e}")
        results['evidence']['pari_analytic_rank'] = 'Error'
       
    # --- 4. 3-Torsion Analysis (using GAP via Sage) ---
    # The presence of rational 3-torsion points can influence the 3-Selmer group.
    try:
        torsion_subgroup = E.torsion_subgroup()
        torsion_order = torsion_subgroup.order()
        has_3_torsion = (torsion_order % 3 == 0)
        results['evidence']['has_rational_3_torsion'] = has_3_torsion
        print(f"[Step 4] Rational 3-Torsion Points Present: {has_3_torsion} (Torsion Order: {torsion_order})")
    except Exception as e:
        print(f"[Step 4] Torsion analysis failed: {e}")
        results['evidence']['has_rational_3_torsion'] = 'Error'


    # --- 5. The 3-Selmer Proxy: Simulated Advanced Descent (The Workaround) ---
    # This step simulates calling a specialized, open-source script that performs
    # a 3-isogeny descent, a known (but complex) method for bounding the 3-Selmer rank.
    # In a real implementation, this would call an external library or a complex
    # set of functions based on recent number theory research.
    print("[Step 5] Simulating advanced 3-isogeny descent (Magma-free proxy)...")
    try:
        # Heuristic Rule: If 2-Selmer and Analytic Ranks agree and are high,
        # it provides strong evidence that the true rank is high, and therefore
        # the 3-Selmer rank must be at least that high.
        rank_evidence = [r for r in [
            results['evidence'].get('sage_algebraic_rank'),
