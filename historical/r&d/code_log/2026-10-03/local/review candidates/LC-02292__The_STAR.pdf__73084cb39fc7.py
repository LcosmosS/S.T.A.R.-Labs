            with open(ebv_cache_file, 'wb') as f:
                pickle.dump(ebv, f)
            print(f"Cached EBV values to {ebv_cache_file}.")
        except Exception as e:
            print(f"Failed to compute EBV due to {e}. Will use fallback.")
            ebv = None
    else:
        ebv = None
# Fallback if ebv computation failed
