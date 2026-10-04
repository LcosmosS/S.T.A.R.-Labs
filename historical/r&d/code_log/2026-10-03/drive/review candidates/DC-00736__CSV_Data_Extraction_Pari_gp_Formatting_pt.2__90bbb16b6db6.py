    print("Possible similar columns:", similar_columns)
    if 'MANGID' in df_mangahi.columns:
        print("Found 'MANGID', using for join")
        merge_key = 'MANGID'
    else:
        print("No suitable key found, please check column names")
        exit(1)
else:
    merge_key = 'mangaid'
