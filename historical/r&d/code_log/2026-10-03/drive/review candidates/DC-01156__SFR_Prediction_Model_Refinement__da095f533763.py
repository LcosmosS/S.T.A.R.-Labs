import matplotlib.pyplot as plt


plt.scatter(y_test, y_pred, alpha=0.6)
plt.xlabel("Actual SFR")
plt.ylabel("Predicted SFR")
plt.title("Actual vs Predicted Star Formation Rate")
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'r--')
plt.savefig("actual_vs_predicted.png")
