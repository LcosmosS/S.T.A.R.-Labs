import numpy as np
from scipy.optimize import curve_fit


# Assuming `bsd_likelihood` and `sfr` are numpy arrays
def exponential(x, a, b, c):
    return a * np.exp(b * x) + c


params, _ = curve_fit(exponential, bsd_likelihood, sfr, maxfev=10000)
x_fit = np.linspace(min(bsd_likelihood), max(bsd_likelihood), 100)
y_fit = exponential(x_fit, *params)


plt.scatter(bsd_likelihood, sfr, alpha=0.3, color="blue")
plt.plot(x_fit, y_fit, color="red", label="Exponential fit")
plt.xlabel("BSD Likelihood (symbolic)")
plt.ylabel("Star Formation Rate (SFR)")
plt.title("BSD-inspired Metric vs SFR")
plt.legend()
plt.show()
