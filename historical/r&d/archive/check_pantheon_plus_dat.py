from src.likelihoods.data import pantheon_plus  # or from src.likelihoods.data.pantheon_plus import PANTHEON_PLUS_FULL
from src.likelihoods.data.pantheon_plus import PANTHEON_PLUS_FULL

# Quick prints
print("Type of PANTHEON_PLUS_FULL:", type(PANTHEON_PLUS_FULL))
print("Keys:", list(PANTHEON_PLUS_FULL.keys()))

# Show first 10 z values and types
z_sample = PANTHEON_PLUS_FULL.get("z", [])[:20]
print("z sample:", z_sample)
print("z types:", [type(x) for x in z_sample])

# Find any non-numeric entries
bad_idx = [i for i,x in enumerate(z_sample) if not isinstance(x, (int,float))]
print("Non-numeric indices in sample:", bad_idx)

# Full scan (may be slow but definitive)
bad_all = [i for i,x in enumerate(PANTHEON_PLUS_FULL.get("z", [])) if not isinstance(x, (int,float))]
print("Total non-numeric z entries:", len(bad_all))
if bad_all:
    print("First bad index and value:", bad_all[0], PANTHEON_PLUS_FULL["z"][bad_all[0]])
