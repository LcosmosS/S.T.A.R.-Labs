    print(header)
    print("-" * len(header))
    for _, row in df.iterrows():
        row_str = "".join([f"{str(row[col]):<{width}}" for col, width in
col_widths.items()])
        print(row_str)

if __name__ == '__main__':
    hypothesis_test_pipeline()
