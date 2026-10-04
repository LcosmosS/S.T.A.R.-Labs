import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
data = pd.read_csv("interweb_nodes.txt")
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(data['rank'], data['log_delta'], data['log_cond'], s=data['leading_coeff'])
   * plt.show()
