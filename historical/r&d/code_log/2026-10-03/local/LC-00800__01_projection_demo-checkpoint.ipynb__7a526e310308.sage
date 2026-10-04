# --- CI + arithmetic archive detection ---
RUNNING_IN_CI = os.environ.get("GITHUB_ACTIONS", "false") == "true"

# --- Submodule paths ---
ECDATA = "data/ecdata"
LMFDB = "data/lmfdb"
CI_LABELS = "data/raw/ci_subset.csv"

print("Running in CI:", RUNNING_IN_CI)
print("Cremona ecdata:", os.path.exists(ECDATA))
print("LMFDB:", os.path.exists(LMFDB))
print("CI labels:", os.path.exists(CI_LABELS))
