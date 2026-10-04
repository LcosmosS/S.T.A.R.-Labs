def symbolic_entropy(vec):
    p = vec / vec.sum()
    return -np.sum(p * np.log(p))
