
**Interpretation**:
- Projection identity space formed naturally from category treatment;
- Performance improved in morphological degeneracy zones;
- Entropy layering was cleaner across high-variance symbolic attractor regimes.

**Results**:
- Test R²: 0.857
- SHAP structure: Strong consistency with entropy basin attractors
- Symbolic error alignment improved near morphology-redshift transition edges.

-----------------------------------------
III. LIGHTGBM – ENTROPY-AWARE BOOSTING EFFICIENCY

LightGBM’s histogram-based leaf-wise tree growth approximated entropy stratification naturally.

```python
import lightgbm as lgb

lgb_model = lgb.LGBMRegressor(num_leaves=64, learning_rate=0.03, n_estimators=300)
lgb_model.fit(X_train, y_train)
