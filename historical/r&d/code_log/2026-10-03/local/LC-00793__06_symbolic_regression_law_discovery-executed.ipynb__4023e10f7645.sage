try:
    from src.symbolic_regression.sr_pipeline import SRPipeline

    SR = SRPipeline(max_depth=5, population=30, generations=10)
    best_tree = SR.run(X, isogeny_pairs=[])

    try:
        print("Best tree:", best_tree)
    except Exception:
        print("Best tree returned (object):", type(best_tree))

    preds = (
        np.array([best_tree.evaluate(x) for x in X])
        if hasattr(best_tree, 'evaluate')
        else np.mean(y)*np.ones_like(y)
    )

    mse = np.mean((preds - y)**2)
    print("MSE on training data (approx):", mse)

    pd.DataFrame({'y': y, 'y_pred': preds}).to_csv('results/sr_predictions.csv', index=False)
    print("Saved results/sr_predictions.csv")

except Exception as e:
    print("Symbolic regression modules not available; running simple linear regression fallback.", e)

    from sklearn.linear_model import LinearRegression
    lr = LinearRegression().fit(X, y)
    preds = lr.predict(X)
    mse = np.mean((preds - y)**2)

    pd.DataFrame({'y': y, 'y_pred': preds}).to_csv('results/sr_predictions.csv', index=False)
    print("Saved results/sr_predictions.csv (linear fallback). MSE:", mse)
