def estimate_rank_category(E):
    if not isinstance(E, EllipticCurve): return 'Invalid Curve'
    try:
        rank = E.rank()
        if rank >= 3: return 'Rank 3+'
        elif rank == 2: return 'Rank 2'
        elif rank == 1: return 'Rank 1'
        else: return 'Rank 0'
    except: return 'Computationally Difficult'
