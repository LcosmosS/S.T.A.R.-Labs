modes = scalar_modes[:,0] + scalar_modes[:,1]

fft = np.fft.rfft(modes - np.mean(modes))
ps = np.abs(fft)**2
freqs = np.fft.rfftfreq(len(modes), d=1.0)

plt.figure(figsize=(6,4))
plt.loglog(freqs[1:], ps[1:], '-o', markersize=3)
plt.xlabel('k (arb)')
plt.ylabel('Power')
plt.title('Symbolic Power Spectrum')
plt.savefig('results/symbolic_power_spectrum.png', dpi=200)
plt.show()
