    print("\n--- STAGE 4: Mathematical Fine-Tuning (Anthropic Test) ---")
    df = pd.DataFrame.from_dict(ucf_data, orient='index', columns=[
        'Rank', 'Regulator', 'Comoving_Volume', 'L_value', 'Density_Height', 'Type',
        'Stellar_Mass', 'Rot_Vel', 'Vel_Disp', 'Eff_Rad', 'Surf_Bright', 'Galaxy_Type'
    ])

    df['stability_score'] = df.apply(lambda row: model_universe_stability(row['Rank'],
