traces = np.array([np.trace(dg) for dg in delta_g])

plt.figure(figsize=(6,5))
plt.hist(traces, bins=40, color='C3')
plt.title("Trace(δg) Distribution")
plt.savefig('figures/metric_trace.png', dpi=200)
plt.show()
