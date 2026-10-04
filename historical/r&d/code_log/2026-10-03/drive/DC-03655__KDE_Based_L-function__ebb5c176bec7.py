def objective_rf(trial):
    try:
        model = ...
        score = cross_val_score(model, X_train_scaled, y_train, ...)
        if np.isnan(score).any():
            raise optuna.TrialPruned()
        return np.mean(score)
    except Exception as e:
        print("Trial failed:", e)
        raise optuna.TrialPruned()
