    all_results.append(analyze_3_selmer_evidence(curve_rank2, "y^2 = x^3 + 5x + 144"))

    # --- Print Final Summary ---
    print("\n\n" + "="*80)
    print("                      FINAL 3-SELMER ANALYSIS SUMMARY")
    print("="*80)
    for res in all_results:
        print(f"\nCurve: {res['curve_name']}")
        print(f"  > Final Estimated 3-Selmer Rank (Lower Bound):
