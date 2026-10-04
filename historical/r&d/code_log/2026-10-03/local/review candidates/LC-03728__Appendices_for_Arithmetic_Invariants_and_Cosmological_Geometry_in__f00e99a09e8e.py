    print(f"  > Querying for '{cluster_name}' (a={a}, b={b})...")

    try:
        # Use a session for more robust connection handling
        session = requests.Session()
        # Set a longer timeout and headers to mimic a browser
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = session.get(query_url, timeout=30, headers=headers)
        response.raise_for_status() # Check for HTTP errors like 404 or 500
