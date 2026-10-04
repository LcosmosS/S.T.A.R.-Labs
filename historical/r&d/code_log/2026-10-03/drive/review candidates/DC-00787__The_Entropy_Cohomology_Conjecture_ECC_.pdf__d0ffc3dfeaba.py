import matplotlib.pyplot as pltplt.hexbin(X_test['log_Mass_gas'], X_test['L_cosmo(s)'], C=np.abs(y_test - preds), gridsize=50,
cmap='viridis')
plt.title("Projection-Space Residual Intensity (Gradient Boosting)")
plt.xlabel("log_Mass_gas")
plt.ylabel("L_cosmo(s)")
plt.colorbar(label="Residual Magnitude")
plt.show()
