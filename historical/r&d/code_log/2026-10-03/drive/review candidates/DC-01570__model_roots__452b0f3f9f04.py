m0 = np.median(masses)
sum_mi_m0 = np.sum(masses / m0)
sum_m0_mi = np.sum(m0 / masses)
return sum_mi_m0 / sum_m0_mi
def cosmological_l_function(data, s): """ Computes the cosmological L-function.
