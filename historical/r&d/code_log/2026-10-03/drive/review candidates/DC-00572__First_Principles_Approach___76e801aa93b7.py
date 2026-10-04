        corr, p_val = pearsonr(ucf_recursive_volumes, qft_recursive_complexity)
        results['Recursive_Type'] = {'correlation': corr, 'p_value': p_val}
        print(f"  > Recursive Type Correlation (Volume vs QFT): {corr:.4f} (p={p_val:.4f})")


    return results


def test_unified_gr_correlation(ucf_data):
    """
    Tests the correlation between comoving volume and a GR model that
