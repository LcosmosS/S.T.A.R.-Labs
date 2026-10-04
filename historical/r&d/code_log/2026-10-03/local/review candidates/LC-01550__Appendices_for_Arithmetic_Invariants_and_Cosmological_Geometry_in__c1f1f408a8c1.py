    except Exception as e:
        print(f"[Step 1] SageMath Rank computation failed: {e}")
        results['evidence']['sage_algebraic_rank'] = 'Error'

    # --- 2. PARI/GP Backend: 2-Selmer Rank ---
    # The 2-Selmer rank is a robust upper bound for the true rank.
    try:
        # Use the PARI interface directly for a robust check
        pari_E = pari(E)
        selmer_2_rank = pari_E.ellrank()[1] # ellrank() returns [rank, 2-Selmer rank,
...]
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
        print(f"[Step 4] Rational 3-Torsion Points Present: {has_3_torsion} (Torsion
