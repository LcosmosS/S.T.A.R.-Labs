    try:
        curve = EllipticCurve(QQ, [a, rho])
        rank = curve.rank()
        if rank == 0:
            return {"rank": 0, "regulator": 1.0, "type": "N/A", "curve": curve}
       
        regulator = curve.regulator()
        generator = curve.gens()[0]
       
        is_integer_generator = all(coord.is_integer() for coord in generator.xy())
        structure_type = "Simple" if is_integer_generator else "Recursive"
       
        return {"rank": rank, "regulator": regulator, "type": structure_type}
    except Exception as e:
        print(f"    - ERROR analyzing curve for {name}: {e}")
        return None


def calculate_arithmetic_state(rank, regulator):
    """Calculates the UCF's raw prediction, f(Rank, Regulator)."""
    if rank == 0: return 0
    return RR(regulator / rank) # Use Sage's RealField for precision


# ==============================================================================
# SECTION 3: MAIN PIPELINE EXECUTION
# ==============================================================================


if __name__ == "__main__":
    print("="*80)
    print("          UCF Final Unified Test: Calibrating the Xi (Ξ) Constant")
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
        analysis_result = derive_and_analyze_curve(name, data['r'], data)
       
        if analysis_result:
            arithmetic_state = calculate_arithmetic_state(
                analysis_result['rank'], analysis_result['regulator']
            )
            structure_type = analysis_result['type']
            print(f"  > Arithmetic State (Reg/Rank): {arithmetic_state:.4f} (Type: {structure_type})")
           
            # 3. Predict the Physical Ratio using the full UCF model
            predicted_ratio = arithmetic_state / UPSILON
           
            # 4. Measure the structure-dependent scaling constant, Xi (Ξ)
            # This is the residual error of the model, which should now be close to 1
            if predicted_ratio == 0:
                xi_constant = 0
            else:
                xi_constant = physical_ratio / predicted_ratio


            print(f"  > Predicted Physical Ratio (Arith / ϒ): {predicted_ratio:.4f}")
            print(f"  > Final Scaling Constant (Ξ = Phys / Pred): {xi_constant:.2f}")


            results_list.append({
                'System': name,
                'Structure Type': structure_type,
                'Physical Ratio': RR(physical_ratio),
                'Arithmetic State': RR(arithmetic_state),
                'Xi (Ξ)': RR(xi_constant)
            })


    # --- Final Analysis: Test the Hypothesis ---
    results_df = pd.DataFrame(results_list)
    # ERROR FIX: Convert all columns to a numeric type that pandas can handle
    for col in ['Physical Ratio', 'Arithmetic State', 'Xi (Ξ)']:
        results_df[col] = pd.to_numeric(results_df[col], errors='coerce')
       
    print("\n\n" + "="*80)
    print("                    PIPELINE RESULTS SUMMARY")
    print("="*80)
    print(results_df.to_string(index=False))


    print("\n\n" + "="*80)
    print("                  HYPOTHESIS TEST: STABILITY OF Ξ")
    print("="*80)
   
    grouped = results_df.groupby('Structure Type')
   
    for name, group in grouped:
        if name == "N/A" or len(group) == 0: continue
       
        mean_xi = group['Xi (Ξ)'].mean()
       
        print(f"\n--- Analysis for '{name}' Type Structures ---")
        print(f"  > Number of data points: {len(group)}")
        print(f"  > Mean value of Ξ: {mean_xi:.2f}")
       
        # ERROR FIX: Only calculate standard deviation if there is more than one point
        if len(group) > 1:
            std_xi = group['Xi (Ξ)'].std()
            print(f"  > Standard Deviation of Ξ: {std_xi:.2f}")
            # Check for consistency (low standard deviation relative to the mean)
            if (std_xi / mean_xi) < 0.2: # Allow 20% variance
                print("  > \033[92mRESULT: The value of Ξ is consistent for this structure type.\033[0m")
            else:
                print("  > \033[91mRESULT: The value of Ξ is NOT consistent for this structure type.\03-m")
        else:
            print("  > Not enough data to test for consistency.")




    print("\n\nExecution complete. A mean value of Ξ near 1.0 with low std dev validates the theory.")
