# --- Combined CI‑Aware Loader ---
def load_arithmetic_invariants():
    # 1. Cremona ecdata
    if os.path.exists(ECDATA):
        print("Using Cremona ecdata submodule")
        labels = load_cremona_labels()[:1000]
        return load_invariants_from_submodules(labels), "cremona_ecdata"

    # 2. LMFDB archive
    if os.path.exists(LMFDB):
        print("Using LMFDB submodule")
        labels = load_lmfdb_labels()[:1000]
        return load_invariants_from_submodules(labels), "lmfdb"

    # 3. CI labels
    if RUNNING_IN_CI and os.path.exists(CI_LABELS):
        print("Using CI-generated labels")
        labels = pd.read_csv(CI_LABELS)["label"].tolist()
        return load_invariants_from_submodules(labels), "ci_labels"

    # 4. Synthetic fallback
    print("Using synthetic invariants")
    n = 300
    df = pd.DataFrame({
        "rank": np.random.randint(0,4,size=n),
        "regulator": np.random.exponential(size=n),
        "conductor": np.random.lognormal(5,1,size=n),
    })
    return df, "synthetic"

df, source = load_arithmetic_invariants()
print("Arithmetic source:", source)
df.head()
