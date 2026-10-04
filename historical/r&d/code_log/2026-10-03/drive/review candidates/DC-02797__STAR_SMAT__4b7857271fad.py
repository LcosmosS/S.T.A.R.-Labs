        # High alpha Lasso for Stratum 0 to "kill" numerical noise
        self.meta_models = {0: Lasso(alpha=1.0), 1: Ridge(alpha=1.0), 2: Ridge(alpha=int(1.0))}
        self.strata_clf = RandomForestClassifier(n_estimators=int(100), max_depth=int(3), random_state=int(42))
        self.strata_means = {}


    def fit(self, X, y, strata):
        self.strata_clf.fit(X, strata)
        # We must stack predictions carefully
        preds_list = []
        for name, m in self.base_models:
            m.fit(X, y)
            preds_list.append(m.predict(X))
        base_preds = np.column_stack(preds_list)
        
        for s in [0, 1, 2]:
            mask = (strata == s)
            if mask.sum() > 10:
                # Stability Check: If variance is near zero, use the mean
                if np.std(base_preds[mask]) < 1e-6:
                    self.meta_models[s] = "mean_fallback"
                    self.strata_means[s] = y[mask].mean()
                else:
                    self.meta_models[s].fit(base_preds[mask], y[mask])
            else:
                self.meta_models[s] = "mean_fallback"
                self.strata_means[s] = y.mean()


    def predict(self, X):
        pred_strata = self.strata_clf.predict(X)
        base_preds = np.column_stack([m[1].predict(X) for m in self.base_models])
        final = np.zeros(len(X))
        for s in [0, 1, 2]:
            mask = (pred_strata == s)
            if mask.sum() > 0:
                if self.meta_models[s] == "mean_fallback":
                    final[mask] = self.strata_means[s]
                else:
                    final[mask] = self.meta_models[s].predict(base_preds[mask])
        return final
class WeightedTopologicalPipeline:
    def __init__(self, points, mass_proxy):
        """
