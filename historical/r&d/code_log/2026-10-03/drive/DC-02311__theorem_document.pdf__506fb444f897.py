import numpy as np
import matplotlib.pyplot as plt
r = np.linspace(0.1, 100, 100)
nfw = 1 / (r * (1 + r)**2)
acsc_correction = 1 + 0.05 * np.sin(0.2 * r)
acsc_profile = nfw * acsc_correction
plt.plot(r, nfw, label='Standard NFW')
plt.plot(r, acsc_profile, label='ACSC Prediction')
plt.xlabel('Radius (kpc)')
plt.ylabel('Density (arbitrary units)')
plt.legend()
plt.title('Dark Matter Halo Profiles: Standard vs. ACSC')
plt.show()
