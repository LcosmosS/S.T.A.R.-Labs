import numpy as np
df['sfr'] = df['sfr'].replace(-9999, np.nan)  # Mark -9999 as missing
            * avg_sfr = np.nanmean(df['sfr'])  # Average, ignoring NaN
