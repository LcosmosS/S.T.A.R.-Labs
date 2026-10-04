def local_factor(p, ap):
return -np.log(abs(ap)) / p if ap != 0 else 0
entropy = sum(local_factor(p, ap)
