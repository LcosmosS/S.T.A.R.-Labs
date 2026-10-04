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
