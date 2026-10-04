# ====================== KNN IMPUTATION (physically consistent) ======================
from sklearn.impute import KNNImputer


print("\n🧼 KNN imputation on all features (k=10, using local cosmic neighborhood)...")
imputer = KNNImputer(n_neighbors=10, weights='distance')


# Impute on each dataset separately
for df, name in [(synth, "synth"), (real1, "real1"), (real2, "real2")]:
