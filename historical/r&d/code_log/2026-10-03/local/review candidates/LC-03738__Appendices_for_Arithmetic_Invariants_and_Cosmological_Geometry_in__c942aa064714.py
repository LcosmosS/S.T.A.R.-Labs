        radius_m = chunk.loc[valid_data, 'radius_ly'] * 9.461e15
        mass_kg = chunk.loc[valid_data, 'mass_sm'] * 1.989e30
        volume_m3 = (4/3) * np.pi * (radius_m ** 3)
        chunk.loc[valid_data, 'density_kg_m3'] = mass_kg / volume_m3

        distance_mly = chunk['distance_mpc'] * 3.26156
        coeffs = chunk.apply(lambda row:
map_physics_to_curve_coeffs(distance_mly.get(row.name), row['density_kg_m3']), axis=1)
        chunk[['coeff_a', 'coeff_b']] = pd.DataFrame(coeffs.tolist(),
index=chunk.index)

        def process_curve(row):
            if pd.isna(row['coeff_a']) or pd.isna(row['coeff_b']): return np.nan
