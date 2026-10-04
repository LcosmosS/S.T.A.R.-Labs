        ax.set_xlim(0, 1.0)
        if i == 0: ax.set_ylabel("Homology Groups ($H_0, H_1$)")
        ax.legend(loc='lower right', fontsize='small')

    plt.suptitle("Foliation Test: Persistence Barcode Signature (Real2)", fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('topological_barcodes.png')
    plt.show()

# ====================== MULTI-OBJECTIVE OPTUNA WITH WASSERSTEIN
======================
def objective(trial):
    param = {
        'n_estimators': int(trial.suggest_int('n_estimators', 400, 800)),
        'learning_rate': float(trial.suggest_float('learning_rate', 0.01, 0.05)),
        'max_depth': int(trial.suggest_int('max_depth', 4, 7)),
        'subsample': float(trial.suggest_float('subsample', 0.6, 0.95)),
        'random_state': 42
    }
    kf = KFold(n_splits=int(5), shuffle=True, random_state=int(42))
    mse_scores, r2_scores, w2_scores = [], [], []

    for tr, val in kf.split(synth):
        X_train, y_train = synth[common_features].iloc[tr], synth_y.iloc[tr]
        X_val, y_val = synth[common_features].iloc[val], synth_y.iloc[val]

        model = xgb.XGBRegressor(**param)
        model.fit(X_train, y_train)
        preds = model.predict(X_val)

        mse_scores.append(mean_squared_error(y_val, preds))
        r2_scores.append(r2_score(y_val, preds))
        w2_scores.append(wasserstein_distance(y_val, preds))

    composite_loss = np.mean(mse_scores) + (1.0 - np.mean(r2_scores)) + (2.0 *
np.mean(w2_scores))
    return composite_loss

print("\n Running Multi-Objective Optuna (MSE + (1-R²) + W₂)...")
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=int(15))
best_params = study.best_params
print(f"Best parameters: {best_params}")
