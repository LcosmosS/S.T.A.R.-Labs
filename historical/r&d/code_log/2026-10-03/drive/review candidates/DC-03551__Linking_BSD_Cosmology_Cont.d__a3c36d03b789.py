import matplotlib.pyplot as plt


plt.scatter(y_test, y_pred_refined, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel('Actual log_SFR_Ha')
plt.ylabel('Predicted log_SFR_Ha')
plt.title('Predicted vs. Actual SFR')
plt.savefig('predicted_vs_actual_sfr.png')
* plt.show()
