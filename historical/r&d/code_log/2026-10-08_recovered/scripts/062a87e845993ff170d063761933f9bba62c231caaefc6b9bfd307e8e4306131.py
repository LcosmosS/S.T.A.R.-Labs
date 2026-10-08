import numpy as np

def w2_between_diagrams(dgmA, dgmB):
    # minimal safe fallback: compare number of features
    a = 0 if dgmA is None else len(dgmA)
    b = 0 if dgmB is None else len(dgmB)
    return float(abs(a - b))

def empirical_p_value(observed, null_samples):
    null = np.asarray(null_samples, dtype=float)
    m = len(null)
    count = int((null <= observed).sum())
    return float((1 + count) / (1 + m))
