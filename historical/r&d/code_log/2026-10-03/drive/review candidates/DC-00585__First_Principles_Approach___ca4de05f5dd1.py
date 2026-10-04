    print("\n--- STAGE 4: Mathematical Fine-Tuning (Anthropic Test) ---")
    df = pd.DataFrame.from_dict(ucf_data, orient='index', columns=[
        'Rank', 'Regulator', 'Comoving_Volume', 'L_value', 'Density_Height', 'Type',
        'Stellar_Mass', 'Rot_Vel', 'Vel_Disp', 'Eff_Rad', 'Surf_Bright', 'Galaxy_Type'
    ])
    
    df['stability_score'] = df.apply(lambda row: model_universe_stability(row['Rank'], row['Regulator']), axis=1)
    
    physical_curves = df[df['Galaxy_Type'] != -1]
    unphysical_curves = df[df['Galaxy_Type'] == -1]
    
    avg_stability_physical = physical_curves['stability_score'].mean()
    avg_stability_unphysical = unphysical_curves['stability_score'].mean()
    
    print(f"  > Average stability score for 'Physical' curves (Rank 1): {avg_stability_physical:.4f}")
    print(f"  > Average stability score for 'Un-physical' curves (Rank 0, >1): {avg_stability_unphysical:.4f}")
    
    is_fine_tuned = avg_stability_physical > avg_stability_unphysical * 2 # Require physical to be at least 2x more stable
    print(f"  > Result: The framework {'SUPPORTS' if is_fine_tuned else 'DOES NOT SUPPORT'} the mathematical fine-tuning hypothesis.")
    return {"physical_stability": avg_stability_physical, "unphysical_stability": avg_stability_unphysical, "supports_hypothesis": is_fine_tuned}


# ==============================================================================
# SECTION 4: MAIN EXECUTION
# ==============================================================================


if __name__ == "__main__":
    print("="*60)
    print("   UCF First Principles Validation Pipeline")
    print("="*60)


    # Load all necessary data
    ucf_data = get_ucf_and_physical_data()
    norm_data = get_natural_normalization_data()
    
    # Run all pipeline stages
    stage1_results = run_stage_1_stat_mech_test(norm_data)
    stage2_results = run_stage_2_scaling_law_test(ucf_data)
    stage3_results = run_stage_3_math_physics_context()
    stage4_results = run_stage_4_anthropic_test(ucf_data)


    # Compile final summary
    final_summary = {
        "Stage_1_StatMech_Test": stage1_results,
        "Stage_2_Scaling_Law_Test": stage2_results,
        "Stage_3_Math_Physics_Context": stage3_results,
        "Stage_4_Anthropic_Test": stage4_results
    }
    
    print("\n\n" + "="*60)
    print("                 PIPELINE SUMMARY")
    print("="*60)
    print(json.dumps(final_summary, indent=2))
    print("\nPipeline execution complete.")
