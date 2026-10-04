    print("\n--- STAGE 2: Cosmological Scaling Law Reproduction ---")
    df = pd.DataFrame.from_dict(ucf_data, orient='index', columns=[
        'Rank', 'Regulator', 'Comoving_Volume', 'L_value', 'Density_Height', 'Type',
        'Stellar_Mass', 'Rot_Vel', 'Vel_Disp', 'Eff_Rad', 'Surf_Bright', 'Galaxy_Type'
    ])

    results = {}

    # Test 1: Tully-Fisher for Spiral Galaxies
    spirals = df[df['Galaxy_Type'] == 0]
    if not spirals.empty and len(spirals) > 1:
        print("  > Testing Tully-Fisher Relation (Spirals)...")
        tf_predicted_mass = model_tully_fisher(spirals['Rot_Vel'])
        ucf_regulator = spirals['Regulator']

        corr, p_val = pearsonr(ucf_regulator, np.log10(tf_predicted_mass))
        print(f"    - Correlation(UCF Regulator vs. Predicted Mass): {corr:.4f}
