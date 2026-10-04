        print(f"Rows in {file}: {len(df)}, Columns: {len(df.columns)}")
    except ValueError as e:
        print(f"Error loading {file}: {e}. Check column names.")
        continue

    # Handle Pan-STARRS
    if file in ["PanST2DR1_SDSSDR16.csv", "PanSTDR1_SDSSDR16.csv"]:
        df['nsa_z'] = df['zsp']
        df['g_r'] = df['gmag'] - df['rmag']
        df['P(E)'] = np.where(df['g_r'] > 0.7, 0.8, 0.2)
        df['P(Sc)'] = np.where(df['g_r'] < 0.5, 0.8, 0.2)
