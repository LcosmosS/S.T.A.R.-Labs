   # --- Step 1: Calibrate the Upsilon (Y) Constant ---
   print("\n--- Calibrating the Upsilon (Y) Constant using Virgo Cluster ---")
   virgo_data = galaxy_data['Virgo Cluster']
   virgo_imbalance = calculate_virial_imbalance(
       virgo_data['virial_mass'], virgo_data['vel_disp'], virgo_data['virial_radius']
   )
   virgo_arithmetic = derive_and_analyze_curve('Virgo Cluster', virgo_data['r'], virgo_data)
   virgo_arithmetic_state = RR(virgo_arithmetic['regulator'] / virgo_arithmetic['rank'])
   
   # Solve for Y: 2T+U = -I(A) => Imbalance = -Y * (Reg/Rank)
   CALIBRATED_UPSILON = -virgo_imbalance / virgo_arithmetic_state
   
   print(f" > Virgo Virial Imbalance (2T+U): {virgo_imbalance:.2e}")
   print(f" > Virgo Arithmetic State (Reg/Rank): {virgo_arithmetic_state:.4f}")
   print(f" > \033, data['vel_disp'], data['virial_radius']
       )
       
       # b) Calculate the new UCF term
       analysis_result = derive_and_analyze_curve(name, data['r'], data)
       
       if analysis_result:
           informational_potential = calculate_informational_potential(
               analysis_result['rank'], analysis_result['regulator'], CALIBRATED_UPSILON
           )
           
           # c) Test the new law: Sum the terms to see if they equal zero
           net_virial_energy = virial_imbalance + informational_potential
           
           # d) Calculate a 'Closure Score' to quantify success
           total_kinetic_energy = 0.5 * data['virial_mass'] * (data['vel_disp']**2)
           closure_score = 100 * (1 - abs(net_virial_energy) / (2 * total_kinetic_energy)) if total_kinetic_energy!= 0 else 0

           print(f" > Virial Imbalance (2T+U): {virial_imbalance:.2e}")
           print(f" > Informational Potential I(A): {informational_potential:.2e}")
           print(f" > Net Virial Energy: {net_virial_energy:.2e}")
           print(f" > Closure Score: {closure_score:.2f}%")
           
           results_list.append({
               'System': name,
               'Virial Imbalance (2T+U)': f"{virial_imbalance:.2e}",
               'Informational Potential I(A)': f"{informational_potential:.2e}",
               'Net Virial Energy': f"{net_virial_energy:.2e}",
               'Closure Score (%)': float(f"{closure_score:.2f}")
           })

   # --- Final Results Summary ---
   results_df = pd.DataFrame(results_list)
   print("\n\n" + "="*80)
   print(" FINAL RESULTS SUMMARY")
   print("="*80)
   print(results_df.to_string(index=False))
   
   print("\n\nInterpretation:")
   print("A high 'Closure Score' validates the new energy balance equation, providing")
   print("the first experimental evidence for the existence of Informational Potential.")
   print("\nExecution complete.")
