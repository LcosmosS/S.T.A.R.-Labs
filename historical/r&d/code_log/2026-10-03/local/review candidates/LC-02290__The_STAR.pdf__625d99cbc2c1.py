ebv_cache_file = "ebv_cache.pkl"

# Check if cached ebv values exist
========================================================================
========================================================================
==
if os.path.exists(ebv_cache_file):
    print(f"Loading cached EBV values from {ebv_cache_file}...")
    with open(ebv_cache_file, 'rb') as f:
        ebv = pickle.load(f)
else:
# = Initialize SFDQuery
========================================================================
========================================================================
=============
    try:
        sfd = SFDQuery()
    except FileNotFoundError:
        print("SFD dustmap not found. Fetching now...")
        try:
            import dustmaps.sfd
            dustmaps.sfd.fetch()
            sfd = SFDQuery()
        except Exception as e:
            print(f"Failed to fetch SFD dustmap due to {e}. Will use fallback.")
            sfd = None
    except Exception as e:
        print(f"Failed to initialize SFDQuery due to {e}. Will use fallback.")
        sfd = None
# = Compute ebv values ---------------------------------------------------------------------------------------------
    if sfd is not None:
        try:
# ========= Validate coordinates
