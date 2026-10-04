print("Applying galactic extinction correction...")
start_time = time.time()

# Define cache file for ebv values
=========================================================================================
===========================================
ebv_cache_file = "ebv_cache.pkl"

# Check if cached ebv values exist
=========================================================================================
===========================================
if os.path.exists(ebv_cache_file):
    print(f"Loading cached EBV values from {ebv_cache_file}...")
    with open(ebv_cache_file, 'rb') as f:
        ebv = pickle.load(f)
else:
# = Initialize SFDQuery
=========================================================================================
======================================================
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
# ========= Validate coordinates -----------------------------------------------------------------------------------
            if not coords.is_finite().all():
                raise ValueError("Invalid coordinates detected in SkyCoord object.")
            ebv = sfd(coords)
            ebv = np.array(ebv, dtype=np.float32)
# ======== Validate ebv values --------------------------------------------------------------------------------------
            ebv = np.where(np.isfinite(ebv) & (ebv >= 0), ebv, 0.0)  # Replace NaN/inf and negative values with 0
# ======== Cache the ebv values --------------------------------------------------------------------------------------
            with open(ebv_cache_file, 'wb') as f:
                pickle.dump(ebv, f)
            print(f"Cached EBV values to {ebv_cache_file}.")
        except Exception as e:
            print(f"Failed to compute EBV due to {e}. Will use fallback.")