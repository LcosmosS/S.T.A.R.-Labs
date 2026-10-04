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
