def normalize_point(P):
    x, y, z = P
    return (x/z, y/z, 1) if z != 0 else P
