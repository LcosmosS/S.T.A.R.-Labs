import seaborn as sns
import matplotlib.pyplot as plt
sns.pairplot(df)
* plt.show()
* Parallel Coordinates Plot: Displays all features in a 2D view.
* python
from pandas.plotting import parallel_coordinates
parallel_coordinates(df, class_column='some_label')  # Optional class column
* plt.show()
* Radar Chart: Compares multiple variables for a few data points.
* python
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
* 3D Scatter Plot with Dimensionality Reduction: For high-dimensional data, reduce to 3D using PCA.
* python
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


pca = PCA(n_components=3)
reduced_data = pca.fit_transform(df)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(reduced_data[:, 0], reduced_data[:, 1], reduced_data[:, 2])
* plt.show()
