import seaborn as sns
   * sns.pairplot(df)
   * For a parallel coordinates plot:
   * python
from pandas.plotting import parallel_coordinates
   * parallel_coordinates(df, class_column='some_class_label')
   * For dimensionality reduction and 3D plotting:
   * python
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


pca = PCA(n_components=3)
reduced_data = pca.fit_transform(df)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
   * ax.scatter(reduced_data[:, 0], reduced_data[:, 1], reduced_data[:, 2])
