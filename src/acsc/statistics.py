import numpy as np

def w2_between_diagrams(dgmA, dgmB):
    """Return a lightweight diagnostic distance based on cardinality only.

    Controlled TDA experiments should use src.acsc.tda_pipeline.persistence_wasserstein.
    """
    a = 0 if dgmA is None else len(dgmA)
    b = 0 if dgmB is None else len(dgmB)
    return float(abs(a - b))

def empirical_p_value(observed, samples):
    """Lower-tail empirical p-value with finite-sample correction."""
    samples = np.asarray(samples, dtype=float)
    if samples.size == 0:
        return 1.0
    if not np.isfinite(observed):
        raise ValueError("observed must be finite")
    count = np.sum(samples <= observed)
    return float((1 + count) / (1 + samples.size))

def effect_size(observed, null_samples):
    """Cohen-like effect size: (mean_null - observed) / std_null."""
    null = np.asarray(null_samples, dtype=float)
    if null.size == 0:
        return 0.0
    mu = float(np.mean(null))
    sigma = float(np.std(null, ddof=1)) if null.size > 1 else 1.0
    return float((mu - observed) / (sigma if sigma > 0 else 1.0))
