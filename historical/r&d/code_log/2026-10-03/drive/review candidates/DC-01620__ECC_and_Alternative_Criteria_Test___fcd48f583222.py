def calculate_distance_mpc(z): 
    if z is None or not np.isfinite(z) or z <= 0: 
        return np.nan, {'Distance': np.nan, 'Status': 'Invalid input'}
    try: 
        distance = float(cosmo.comoving_distance(z).to(u.Mpc).value) 
        return distance, {'Distance': distance, 'Status': 'Computed'}
    except Exception as e: 
        logging.debug(f"calculate_distance_mpc: Error - {str(e)}")
        return np.nan, {'Distance': np.nan, 'Status': f'Error: {str(e)}'}
However, in entropy5.py, calculate_distance_mpc may have been modified to return only the distance value (e.g., np.nan or a Series), causing the unpacking error in process_chunk:
chunk['distance_mpc'], distance_summary = chunk['z'].apply(calculate_distance_mpc)
