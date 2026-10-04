import numpy as np
from scipy.spatial.distance import pdist
rng = np.random.RandomState(42)
idx = rng.choice(len(coords), size=min(2000, len(coords)), replace=False)
d = pdist(coords[idx])
print("distances: min, median, mean, 90pct, max:", d.min(), np.median(d), d.mean(), np.percentile(d,90), d.max())
# optional: quick histogram
import matplotlib.pyplot as plt
plt.hist(d, bins=80); plt.title("Pairwise distance histogram (sample)"); plt.show()
