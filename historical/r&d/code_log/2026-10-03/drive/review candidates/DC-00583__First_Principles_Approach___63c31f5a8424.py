    print("\n--- STAGE 2: Cosmological Scaling Law Reproduction ---")
    df = pd.DataFrame.from_dict(ucf_data, orient='index', columns=[
        'Rank', 'Regulator', 'Comoving_Volume', 'L_value', 'Density_Height', 'Type',
        'Stellar_Mass', 'Rot_Vel', 'Vel_Disp', 'Eff_Rad', 'Surf_Bright', 'Galaxy_Type'
    ])


    # Test 1: Tully-Fisher for Spiral Galaxies
    spirals = df[df['Galaxy_Type'] == 0]
    if not spirals.empty:
        print("  > Testing Tully-Fisher Relation (Spirals)...")
        tf_predicted_mass = model_tully_fisher(spirals['Rot_Vel'])
        ucf_regulator = spirals['Regulator']
        
        # We test if the UCF regulator scales with the mass predicted by physics
        corr, p_val = pearsonr(ucf_regulator, np.log10(tf_predicted_mass))
        print(f"    - Correlation(UCF Regulator vs. Predicted Mass): {corr:.4f} (p={p_val:.4f})")
    
    # Test 2: Fundamental Plane for Elliptical Galaxies
    ellipticals = df[df['Galaxy_Type'] == 1]
    if not ellipticals.empty:
        print("  > Testing Fundamental Plane (Ellipticals)...")
        fp_predicted_mass = model_fundamental_plane(ellipticals['Vel_Disp'], ellipticals['Eff_Rad'])
        ucf_regulator = ellipticals['Regulator']
        
        corr, p_val = pearsonr(ucf_regulator, np.log10(fp_predicted_mass))
        print(f"    - Correlation(UCF Regulator vs. Predicted Mass): {corr:.4f} (p={p_val:.4f})")
    
    # Store and return results
    return {
        "tully_fisher_corr": pearsonr(spirals['Regulator'], np.log10(model_tully_fisher(spirals['Rot_Vel'])))[0],
        "fundamental_plane_corr": pearsonr(ellipticals['Regulator'], np.log10(model_fundamental_plane(ellipticals['Vel_Disp'], ellipticals['Eff_Rad'])))[0]
    }




def run_stage_3_math_physics_context():
    """
    This stage is conceptual, outlining the context for deeper research.
