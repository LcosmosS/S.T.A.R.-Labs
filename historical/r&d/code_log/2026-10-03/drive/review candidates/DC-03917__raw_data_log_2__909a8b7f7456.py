    if cols_to_impute:
        df[cols_to_impute] = imputer.fit_transform(df[cols_to_impute])
        print(f"   {name} — {len(cols_to_impute)} columns imputed with KNN")
