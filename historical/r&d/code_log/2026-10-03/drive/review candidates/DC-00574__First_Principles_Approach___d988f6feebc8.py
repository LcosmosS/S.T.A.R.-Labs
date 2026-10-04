    gr_curvatures = model_gr_unified(density_heights)
    
    corr, p_val = pearsonr(ucf_volumes, gr_curvatures)
    print(f"  > Correlation (Volume vs Density-Height-Derived Curvature): {corr:.4f}")
    print(f"  > P-value: {p_val:.4f}")
    return {"correlation": corr, "p_value": p_val}


def test_bsd_structural_isomorphism(cosmo_bsd_data):
    """Validates the structural integrity of the Cosmological BSD Analogue."""
    print("\nRunning BSD Structural Isomorphism Test...")
    k_value = cosmo_bsd_data['Large_Scale_Study'][2]
    score = 1 / (1 + abs(1 - k_value))
    print(f"  > Cosmological Analogue's K value: {k_value:.4f}")
    print(f"  > Isomorphism Score: {score:.4f}")
    return {"isomorphism_score": score, "k_value": k_value}


# ==============================================================================
# SECTION 4: MAIN EXECUTION
# ==============================================================================


if __name__ == "__main__":
    print("="*60)
    print("   Advanced Validation Pipeline for the UCF (v2.0)")
    print("="*60)


    # Load enhanced data
    ucf_data = get_enhanced_ucf_data()
    cosmo_bsd_data = get_cosmological_bsd_analogue_data()


    # Run the new, more sophisticated tests
    qft_results = test_type_aware_qft_correlation(ucf_data)
    gr_results = test_unified_gr_correlation(ucf_data)
    bsd_results = test_bsd_structural_isomorphism(cosmo_bsd_data)


    # --- ERROR FIX: Correctly define the results dictionary ---
    all_results = {
        "Type_Aware_QFT_Correlation": qft_results,
        "Unified_GR_Correlation": gr_results,
        "BSD_Isomorphism": bsd_results
    }


    print("\n\n" + "="*60)
    print("                 PIPELINE SUMMARY")
    print("="*60)
    print(json.dumps(all_results, indent=2))
    print("\nPipeline execution complete.")
