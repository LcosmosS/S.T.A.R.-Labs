    print("\nRunning BSD Structural Isomorphism Test...")
    theoretical_bsd = model_birch_swinnerton_dyer()
    print(f"  > Theoretical BSD Form: {theoretical_bsd}")


    # The 'Natural Normalization' paper shows L_cosmo ~ Product_invariants,
    # which is achieved when the normalization constant K is ~1.
    k_value = cosmo_bsd_data['Large_Scale_Study'][2]
    isomorphism_score = 1 / (1 + abs(1 - k_value)) # Score -> 1 as K -> 1


    print(f"  > Cosmological Analogue's K value: {k_value:.4f}")
    print(f"  > Structural Isomorphism Score (closer to 1 is better): {isomorphism_score:.4f}")
    return {"isomorphism_score": isomorphism_score, "k_value": k_value}


# ==============================================================================
# SECTION 4: MAIN EXECUTION
# ==============================================================================


if __name__ == "__main__":
    print("="*60)
    print("  First Principles Validation Pipeline for the UCF")
    print("="*60)


    # Load data from the framework
    ucf_core_data = get_ucf_data()
    cosmo_bsd_data = get_cosmological_bsd_analogue_data()


    # Run the correlation and validation tests
    qft_results = test_qft_correlation(ucf_core_data)
    gr_results = test_gr_correlation(ucf_core_data)
    bsd_results = test_bsd_structural_isomorphism(cosmo_bsd_data)


    # --- SYNTAX ERROR FIX ---
    # The original line 'results =' was incomplete.
    # It has been corrected to define a dictionary that collects the
    # outputs from the tests above for a clean, final summary.
    results = {
        "QFT_Correlation": qft_results,
        "GR_Correlation": gr_results,
        "BSD_Isomorphism": bsd_results
    }


    print("\n\n" + "="*60)
    print("                 PIPELINE SUMMARY")
    print("="*60)
    import json
    print(json.dumps(results, indent=2))
    print("\nPipeline execution complete.")
