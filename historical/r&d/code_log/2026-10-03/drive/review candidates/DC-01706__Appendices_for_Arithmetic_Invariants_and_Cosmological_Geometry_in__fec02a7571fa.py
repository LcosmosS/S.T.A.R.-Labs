        return


    total_rows_processed = 0
    header_written = False


    print(f"Starting SageMath pipeline for '{INPUT_FILE}'...")
    for i, chunk in enumerate(chunk_iter):
        print(f"Processing chunk {i+1}...")


        chunk.replace(-9999, np.nan, inplace=True)
        required_cols = ['z', 'logmass', 'petrorad_r']
        chunk.dropna(subset=required_cols, inplace=True)
        chunk = chunk[chunk['z'] > 0]


        if not chunk.empty:
            # Derive physical parameters
            chunk['distance_mpc'] = chunk['z'].apply(calculate_distance_mpc)
            chunk['mass_sm'] = chunk['logmass'].apply(convert_logmass_to_sm)
            chunk['radius_ly'] = chunk.apply(lambda row: estimate_radius_ly(row['petrorad_r'], row['distance_mpc']), axis=1)


            # Calculate Virial Energy and Density
            chunk['virial_energy_j'] = chunk.apply(lambda row: calculate_virial_energy(row['mass_sm'], row['radius_ly']), axis=1)


            valid_data = chunk['radius_ly'].notna() & (chunk['radius_ly'] > 0) & chunk['mass_sm'].notna()
            radius_m = chunk.loc[valid_data, 'radius_ly'] * 9.461e15
            mass_kg = chunk.loc[valid_data, 'mass_sm'] * 1.989e30
            volume_m3 = (4/3) * np.pi * (radius_m ** 3)
            chunk['density_kg_m3'] = np.nan
            chunk.loc[valid_data, 'density_kg_m3'] = mass_kg / volume_m3


            # Map to curve and calculate discriminant using SageMath
            distance_mly = chunk['distance_mpc'] * 3.26156
            coeffs = chunk.apply(lambda row: map_physics_to_curve_coeffs(distance_mly.get(row.name), row['density_kg_m3']), axis=1)
            chunk[['coeff_a', 'coeff_b']] = pd.DataFrame(coeffs.tolist(), index=chunk.index)
            chunk['discriminant'] = chunk.apply(lambda row: calculate_sagemath_discriminant(row['coeff_a'], row['coeff_b']), axis=1)


            # Calculate the scaling constant
            chunk['scaling_constant_K'] = chunk['virial_energy_j'] / chunk['discriminant'].astype(float)


            # Define and save output
            output_cols = [
                'objid', 'ra', 'dec', 'z', 'mass_sm', 'radius_ly',
                'distance_mpc', 'virial_energy_j', 'discriminant', 'scaling_constant_K'
            ]


            # Ensure all output columns exist before saving
            for col in output_cols:
                if col not in chunk.columns:
                    chunk[col] = np.nan


            processed_chunk = chunk[output_cols]
            processed_chunk.to_csv(
                OUTPUT_FILE,
                mode='a',
                header=not header_written,
                index=False
            )
            header_written = True


        total_rows_processed += len(chunk)
        if ROW_LIMIT and total_rows_processed >= ROW_LIMIT:
            print(f"Reached row limit of {ROW_LIMIT}. Stopping.")
            break


    print("\nPipeline finished.")
    print(f"Total rows processed from input: {total_rows_processed}")
    print(f"Results saved to '{OUTPUT_FILE}'")
    print(f"\nTo analyze the results, you can now run:\nimport pandas as pd\ndf = pd.read_csv('{OUTPUT_FILE}')\nprint(df.head())\nprint(df['scaling_constant_K'].describe())")


# --- 6. Script Execution ---
if __name__ == "__main__":
    main()
