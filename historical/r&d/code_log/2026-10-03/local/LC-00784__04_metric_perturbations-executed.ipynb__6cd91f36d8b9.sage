plt.figure(figsize=(6,4))
plt.hist(traces, bins=40, color='C3', alpha=0.8)
plt.title('Distribution of trace(δg)')
plt.xlabel('trace')
plt.savefig('results/delta_g_trace_hist.png')
plt.show()

pd.DataFrame({'trace_delta_g': traces}).to_csv('results/delta_g_summary.csv', index=False)
print("Saved results/delta_g_summary.csv and figures.")
