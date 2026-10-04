df = prepare_data(clusters)
print(df[["name", "gen_type", "num_x", "num_y"]])


clf, booster, acc = run_ml_pipeline(df)
