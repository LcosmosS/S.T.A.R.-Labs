    return {
        'Virgo_Analogue':   np.array([1, 0.025, 1.57e5, 0.025, 6320, 0, 11.5, 250, 0, 0, 0, 0]),
        'Coma_Analogue':    np.array([1, 0.98,  3.31e7, 0.98,  9980, 1, 12.0, 0, 950, 100, 22.5, 1]),
        'Perseus_Analogue': np.array([1, 3.86,  2.1e6,  1.0,   7500, 0, 11.8, 0, 800, 90, 22.0, 1]),
        'UGC_2885':         np.array([1, 1.5,   8.2e5,  1.0,   4500, 0, 12.2, 350, 0, 0, 0, 0]), # Giant Spiral
        'M87':              np.array([1, 2.1,   1.9e6,  1.0,   8800, 1, 11.9, 0, 750, 80, 21.5, 1]), # Giant Elliptical
        'Void_Analogue_1':  np.array([0, 0.001, 1e8,    0.001, 100,  0, 0, 0, 0, 0, 0, -1]), # Rank 0 unphysical
        'HighRank_Unphys':  np.array([4, 15.0,  1e10,   1.0,   25000,1, 0, 0, 0, 0, 0, -1]), # High-rank unphysical
    }


def get_natural_normalization_data():
    """
    Returns the key validated parameters from your "Natural Normalization" paper.
