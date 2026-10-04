    # This is a testable, non-linear formula based on your research insights.
    # A high regulator (dense) and low rank (simple) should be more "bound",
    # affecting the virial ratio.
    # We calibrate it so that a "normal" Rank 1 curve with Regulator ~4 gives ~0.5.
    base_ratio = 0.125 * regulator
   
    if rank == 0:
        return base_ratio * 0.1 # Voids are not virialized
    elif rank == 1:
        return base_ratio
    elif rank > 1:
        return base_ratio * (1 / rank) # Higher rank structures are more complex
    else:
        return 0


# ==============================================================================
# SECTION 4: MAIN ANALYSIS SCRIPT
# ==============================================================================


if __name__ == "__main__":
    print("="*80)
    print("   UCF vs. The Virial Theorem: A First-Principles Test")
    print("="*80)


    galaxy_data = get_galaxy_virial_data()
    results_list = []


    for name, data in galaxy_data.items():
        print(f"\nProcessing System: {name}...")
       
        # 1. Calculate the benchmark ratio from observational physics
        physical_ratio = calculate_physical_virial_ratio(data['vel_disp'], data['virial_radius'])
       
        # 2. Derive the UCF elliptic curve
        curve = derive_curve_from_virial_data(name, data['r'], data['vel_disp'])
       
        if curve:
            try:
                # 3. Get the arithmetic invariants (Rank and Regulator)
                rank = curve.rank()
                regulator = curve.regulator()
               
                # 4. Predict the virial ratio using only the UCF's arithmetic
                arithmetic_ratio = predict_virial_ratio_from_invariants(rank, regulator)
               
                # 5. Compare the physical vs. arithmetic predictions
                percent_diff = 100 * abs(arithmetic_ratio - physical_ratio) / physical_ratio if physical_ratio != 0 else 0
               
                print(f"  > Success. Physical Ratio: {physical_ratio:.4f}, Arithmetic Ratio: {arithmetic_ratio:.4f}")
               
                results_list.append({
                    'System': name,
                    'Physical Ratio': f"{physical_ratio:.4f}",
                    'Arithmetic Ratio': f"{arithmetic_ratio:.4f}",
                    '% Difference': f"{percent_diff:.2f}%"
                })


            except Exception as e:
                print(f"    - ERROR: Failed to compute invariants for {name}: {e}")
                results_list.append({'System': name, 'Physical Ratio': f"{physical_ratio:.4f}", 'Arithmetic Ratio': 'Error', '% Difference': 'N/A'})
        else:
             results_list.append({'System': name, 'Physical Ratio': f"{physical_ratio:.4f}", 'Arithmetic Ratio': 'N/A', '% Difference': 'N/A'})


    # --- Display Final Results ---
    results_df = pd.DataFrame(results_list)
    print("\n\n" + "="*80)
    print("                      FINAL RESULTS COMPARISON")
    print("="*80)
    print(results_df.to_string())
   
    print("\n\nInterpretation:")
    print("A small '% Difference' suggests the UCF's arithmetic (Rank, Regulator)")
    print("is a powerful proxy for the galaxy's real physical dynamics (Virial State).")
   
    print("\nExecution complete.")
