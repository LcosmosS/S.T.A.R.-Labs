modes = scalar_modes[:,0] + scalar_modes[:,1]
fft = np.fft.rfft(modes - np.mean(modes))
ps = np.abs(fft)**2
freqs = np.fft.rfftfreq(len(modes), d=1.0)

plt.figure(figsize=(6,5))
plt.loglog(freqs[1:], ps[1:], '-o', markersize=3)
plt.title("Scalar Mode Power Spectrum")
plt.savefig('figures/power_spectrum.png', dpi=200)
plt.show()
