    # The LMFDB can be queried directly by Weierstrass coefficients.
    # The format is a_coeffs=[a1, a2, a3, a4, a6], which for our short form is [0, a, 0, b, 0].
    # However, the search form uses a4 and a6.
    query_url = f"https://www.lmfdb.org/EllipticCurve/Q/?a_coeffs=%5B0%2C+{a}%2C+0%2C+{b}%2C+0%5D"
   
    print(f"  > Querying for '{cluster_name}' (a={a}, b={b})...")
   
    try:
        # Use a session for more robust connection handling
        session = requests.Session()
        # Set a longer timeout and headers to mimic a browser
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = session.get(query_url, timeout=30, headers=headers)
        response.raise_for_status() # Check for HTTP errors like 404 or 500


        # Check the content of the response to determine success
        if ">No elliptic curves found" in response.text or "invalid" in response.text.lower():
            return {"found": False, "lmfdb_label": None, "status": "Not Found in DB"}
        else:
            # Search for the canonical LMFDB label in the page's HTML
            match = re.search(r'href="/EllipticCurve/Q/([^"]+)"', response.text)
            if match:
                lmfdb_label = match.group(1).split('?')[0] # Clean up the label
                return {"found": True, "lmfdb_label": lmfdb_label, "status": "Success"}
            else:
                return {"found": True, "lmfdb_label": None, "status": "Page Found, No Label"}


    except requests.exceptions.Timeout:
        return {"found": False, "lmfdb_label": None, "status": "Error: Connection Timed Out"}
    except requests.exceptions.RequestException as e:
        return {"found": False, "lmfdb_label": None, "status": f"Error: {e}"}


# ==============================================================================
# SECTION 3: MAIN EXECUTION SCRIPT
# ==============================================================================


if __name__ == "__main__":
    print("="*70)
    print("   UCF LMFDB Expansion and Live Query Tool")
    print("="*70)


    cluster_data = get_expanded_cluster_data()
    results_list = []


    for name, data in cluster_data.items():
        # Step 1: Derive curve coefficients from physical data
        a, b = derive_curve_parameters(name, data['r'], data['rho'])
       
        # Step 2: Query the live LMFDB with these coefficients
        # Add a delay to be respectful to the server
        time.sleep(2)
        lmfdb_result = query_lmfdb_by_coeffs(a, b, name)
       
        # Step 3: Store results
        results_list.append({
            'Cluster': name,
            'r (Mly)': data['r'],
            'rho': data['rho'],
            'Derived "a"': a,
            'Derived "b"': b,
            'LMFDB Found': 'Yes' if lmfdb_result['found'] else 'No',
            'LMFDB Label': lmfdb_result['lmfdb_label'] or '---',
            'Query Status': lmfdb_result['status']
        })


    # Display final results in a clean table format
    results_df = pd.DataFrame(results_list)
    print("\n\n" + "="*70)
    print("                 FINAL QUERY RESULTS")
    print("="*70)
    print(results_df.to_string())
    print("\n\nExecution complete. Review the 'LMFDB Found' and 'LMFDB Label' columns.")
