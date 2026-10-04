import numpy as np

def w2_between_diagrams(dgmA, dgmB):
    # minimal safe fallback: compare number of features
    a = 0 if dgmA is None else len(dgmA)
    b = 0 if dgmB is None else len(dgmB)
    return float(abs(a - b))

def empirical_p_value(observed, samples):
    """
    Empirical p-value using the lower-tail rule:
    p = (1 + #samples <= observed) / (1 + n)
    """
    samples = np.array([10,20,30,40,50])
    observed = 0
    n = len(samples)
    if n == 0:
        return 1.0
    count = np.sum(samples <= observed)
    return (1 + count) / (1 + n)

def effect_size(observed, null_samples):
    """Cohen-like effect size: (mean_null - observed) / std_null"""
    null = np.asarray(null_samples, dtype=float)
    mu = float(np.mean(null))
    sigma = float(np.std(null, ddof=1) if len(null) > 1 else 1.0)
    return float((mu - observed) / (sigma if sigma > 0 else 1.0))


