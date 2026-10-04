print("Notebook: 04_metric_perturbations")
print("Data source:",
      "projection_points.csv" if os.path.exists('results/projection_points.csv')
      else "CI labels" if RUNNING_IN_CI else "synthetic")
print("Outputs: results/delta_g_summary.csv, results/symbolic_power_spectrum.png")
