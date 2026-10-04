    print(f"File not found: {file_path}")
    exit(1)


# Try to convert 'objid' to integer
try:
    df['objid'] = df['objid'].astype(float).astype(int)
