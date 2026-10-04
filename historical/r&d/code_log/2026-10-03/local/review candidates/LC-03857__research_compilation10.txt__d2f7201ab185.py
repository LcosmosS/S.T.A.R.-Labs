from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


pca = PCA(n_components=3)
reduced_data = pca.fit_transform(df)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
