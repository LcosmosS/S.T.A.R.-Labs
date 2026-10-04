import numpy as np


# Assume 'groups' and 'z' are your arrays
group1_indices = (groups == 1)
z_group1 = z[group1_indices]
bins = np.percentile(z_group1, [0, 20, 40, 60, 80, 100])  # 5 bins
bin4_mask = (z_group1 >= bins[4]) & (z_group1 <= bins[5])  # Bin 4 range
z_bin4 = z_group1[bin4_mask]
         * print(f"Bin 4 redshift range: {np.min(z_bin4):.4f} to {np.max(z_bin4):.4f}")
