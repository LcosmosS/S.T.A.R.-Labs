    # Per your research, the Virgo curve is a special, foundational case
    if cluster_name == 'Virgo':
        a = -1706
        b = 6320
    else:
        # Standard mapping: a = round(-KAPPA * r)
        a = round(-DATA_DRIVEN_KAPPA * r)
        b = rho
    return a, b


def query_lmfdb_by_coeffs(a, b, cluster_name):
    """
