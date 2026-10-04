                       import pandas as pd
                       import matplotlib.pyplot as plt
                       from mpl_toolkits.mplot3d import Axes3D
                     data = pd.read_csv("interweb_nodes.txt")
                     fig = plt.figure()
                    ax = fig.add_subplot(111, projection='3d')
                  scatter = ax.scatter(data['log_delta'], data['log_cond'], data['rank'], s=data['normalized_leading_coeff']*100, c=data['tamagawa'])
                     plt.colorbar(scatter, label='Tamagawa')
   * plt.show()
