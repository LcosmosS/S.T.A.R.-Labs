    # The refined, non-linear hypothesis from the previous test
    return regulator / rank


# ==============================================================================
# SECTION 3: MAIN PIPELINE EXECUTION
# ==============================================================================


if __name__ == "__main__":
    print("="*80)
    print("      UCF Unified Scaling Law Pipeline: Measuring the Xi (Ξ) Constant")
    print("="*80)


    galaxy_data = get_galaxy_virial_data()
    results_list = []


    for name, data in galaxy_data.items():
        print(f"\nProcessing System: {name}...")
       
        # 1. Calculate the ground truth from first-principles physics
        physical_ratio = calculate_physical_virial_ratio(
            data['virial_mass'], data['vel_disp'], data['virial_radius']
        )
        print(f"  > Physical Virial Ratio (2T/|U|): {physical_ratio:.4f}")


        # 2. Derive and analyze the corresponding UCF curve
        analysis_result = derive_and_analyze_curve(name, data['r'], data['vel_disp'])
       
        if analysis_result:
            rank = analysis_result['rank']
            regulator = analysis_result['regulator']
            structure_type = analysis_result['type']
           
            # 3. Calculate the prediction from the UCF's arithmetic state
            arithmetic_state = calculate_arithmetic_state(rank, regulator)
            print(f"  > Arithmetic State (Reg/Rank): {arithmetic_state:.4f} (Type: {structure_type})")
           
            # 4. Measure the Virial Scaling Constant, Xi (Ξ)
            if arithmetic_state == 0:
                xi_constant = 0
            else:
                xi_constant = physical_ratio / arithmetic_state
            print(f"  > Measured Scaling Constant (Ξ): {xi_constant:.2f}")


            results_list.append({
                'System': name,
                'Structure Type': structure_type,
                'Physical Ratio': physical_ratio,
                'Arithmetic State': arithmetic_state,
                'Xi (Ξ)': xi_constant
            })


    # --- Final Analysis: Test the Hypothesis ---
    results_df = pd.DataFrame(results_list)
    print("\n\n" + "="*80)
    print("                    PIPELINE RESULTS SUMMARY")
    print("="*80)
    print(results_df.to_string(index=False))


    print("\n\n" + "="*80)
    print("                  HYPOTHESIS TEST: STABILITY OF Ξ")
    print("="*80)
   
    # Group results by the classified "Structure Type"
    grouped = results_df.groupby('Structure Type')
   
    for name, group in grouped:
        if name == "N/A": continue
       
        mean_xi = group['Xi (Ξ)'].mean()
        std_xi = group['Xi (Ξ)'].std()
       
        print(f"\n--- Analysis for '{name}' Type Structures ---")
        print(f"  > Number of data points: {len(group)}")
        print(f"  > Mean value of Ξ: {mean_xi:.2f}")
        print(f"  > Standard Deviation of Ξ: {std_xi:.2f}")
       
        # Check for consistency (low standard deviation relative to the mean)
        if len(group) > 1 and (std_xi / mean_xi) < 0.2: # Allow 20% variance for consistency
            print("  > \033[92mRESULT: The value of Ξ is consistent for this structure type.\033[0m")
        elif len(group) > 1:
            print("  > \033[91mRESULT: The value of Ξ is NOT consistent for this structure type.\033[0m")


    print("\n\nExecution complete.")
