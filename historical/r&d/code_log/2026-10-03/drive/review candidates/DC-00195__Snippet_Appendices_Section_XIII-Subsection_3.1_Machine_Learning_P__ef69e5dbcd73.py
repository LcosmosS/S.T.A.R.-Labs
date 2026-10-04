pipeline.fit(X_tf, y_tf)
print("Tully-Fisher R²:", cross_val_score(pipeline, X_tf, y_tf, cv=5, scoring='r2').mean())


# Save results
df.to_csv(f'{OUTPUT_PLOT_PREFIX}_processed.csv', index=False)
