y_scrambled = np.random.permutation(y)

try:
    if 'best_tree' in locals() and hasattr(best_tree, 'evaluate'):
        preds_scr = np.array([best_tree.evaluate(x) for x in X])
    else:
        preds_scr = preds  # fallback

    mse_scr = np.mean((preds_scr - y_scrambled)**2)
    print("Null-scramble MSE (approx):", mse_scr)

except Exception as e:
    print("Null-scramble test skipped:", e)
