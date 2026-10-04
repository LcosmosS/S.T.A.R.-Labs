try:
    from src.entropy.entropy_field import EntropyField
    from src.entropy.entropy_shells import EntropyShells

    M = EntropyField()
    S = EntropyShells(M)

    points = df[['x','y','z']].values
    ent = np.array([M.entropy(p) for p in points])
    grads = np.vstack([M.gradient(p) for p in points])
    hess_traces = np.array([np.trace(M.hessian(p)) for p in points])

    print("Computed entropy, gradients, Hessian traces using src.entropy.")

except Exception as e:
    print("src.entropy not available; using local fallback computations.", e)

    def fallback_entropy(p):
        p = np.abs(p) + 1e-12
        pnorm = p / p.sum()
        return -np.sum(pnorm * np.log(pnorm))

    ent = np.array([fallback_entropy(p) for p in df[['x','y','z']].values])

    # simple fallback gradient
    grads = np.gradient(ent)
    grads = np.vstack([np.ones(3)*g for g in ent])

    hess_traces = np.zeros(len(ent))
