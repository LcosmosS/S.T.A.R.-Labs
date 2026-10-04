                model = model_cls(random_state=42) if mname != 'cat' else model_cls(verbose=0, random_state=42)
                model.fit(X, target)
                r2 = r2_score(target, model.predict(X))
                results[f"{bin_name}_{mname}_{name}"] = r2
        sym = SymbolicRegressor(population_size=500, generations=10,
                                function_set=('add','sub','mul','div','log','sqrt'),
                                metric='mse', random_state=42, verbose=0)
        sym.fit(X, y_b)
        results[bin_name] = {
            'clf_r2': clf_r2,
            'eq_b'  : str(sym._program),
            'n'     : len(bin_df)
        }
        print(f"[{bin_name}] clf_R²={clf_r2:.4f} eq_b={sym._program}")
    df.to_csv(os.path.join(out_dir, "star_v4_full.csv"), index=False)
    return results


# ----------------------------------------------------------------------
# 15. Main driver – FIXED ORDER
# ----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="*S.T.A.R. v4 – FULLY ROBUST")
    parser.add_argument('--input_csv', default='1762061875047A.csv')
    parser.add_argument('--output', default='star_out')
    args = parser.parse_args()


    raw = load_csv(args.input_csv)
    imputer = KNNImputer(n_neighbors=5)
    num_cols = raw.select_dtypes(include=np.number).columns
    raw[num_cols] = imputer.fit_transform(raw[num_cols])


    raw['a'] = raw.get('COEFF2', 1)
    raw['b'] = raw.get('COEFF3', 1)


    sequences = generate_sequences(10)
    sim = raw.apply(lambda row: sequence_similarity(row, sequences), axis=1)
    raw = pd.concat([raw, sim], axis=1)


    hier = [hierarchy_of_evidence(row['a'], row['b']) for _, row in raw.iterrows()]
    raw['alg_rank'], raw['sel2_rank'], raw['sel3_rank'], raw['anal_rank'], raw['converge'], raw['tamagawa_flag'] = zip(*hier)
    raw['rank'] = raw['alg_rank'].fillna(raw['anal_rank']).fillna(0)


    alt = raw.apply(alternative_mappings, axis=1, result_type='expand')
    raw = pd.concat([raw, alt], axis=1)


    # 1. Engineer features FIRST
    raw = engineer_features(raw)


    # 2. NOW assign Omega/T
    raw['Regulator'] = 1.0
    raw['Omega']     = raw['logmass']
    raw['T']         = raw['sfr']


    raw = invariant_scaling(raw)
    raw = inverse_b_design(raw)


    if 'Smooth' not in raw.columns:
        raw['Smooth'] = np.random.uniform(0,1,len(raw))
        raw['Featured'] = 1 - raw['Smooth']
    else:
        raw['Featured'] = 1 - raw['Smooth']


    raw = physics_extensions(raw)
    raw['gen_type'] = raw.apply(bin_generator_type, axis=1)


    results = run_per_bin(raw, args.output)


    try:
        subprocess.run([
            "unity-hub", "--headless", "execute-method",
            "ImportCsvToMesh", os.path.join(args.output, "star_v4_full.csv")
        ], check=True)
    except Exception as e:
        print(f"Unity skipped: {e}")


    print("\n=== FINAL BIN SUMMARY ===")
    for k, v in results.items():
        print(f"{k}: {v}")


if __name__ == '__main__':
    main()
