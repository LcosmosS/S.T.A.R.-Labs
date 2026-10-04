    L, E, s, r, reg, sha, tam = sp.symbols('L E s r reg sha tam')
    bsd_conjecture = sp.Eq(sp.Limit(L(E, s) / (s-1)**r, s, 1), reg * sha * tam)
    return bsd_conjecture




# ==============================================================================
# SECTION 3: CORRELATION AND TESTING PIPELINE
# This section contains the functions that run the actual analysis, comparing
# the UCF data to the first principles models.
# ==============================================================================


def test_qft_correlation(ucf_data):
    """
