import numpy as np
import matplotlib.pyplot as plt
from math import pi


categories = df.columns
values = df.iloc[0].values.flatten().tolist()  # Example for one row
values += values[:1]  # Close the loop
angles = [n / float(len(categories)) * 2 * pi for n in range(len(categories))]
angles += angles[:1]
ax = plt.subplot(111, polar=True)
ax.plot(angles, values)
ax.fill(angles, values, alpha=0.1)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)
* plt.show()
