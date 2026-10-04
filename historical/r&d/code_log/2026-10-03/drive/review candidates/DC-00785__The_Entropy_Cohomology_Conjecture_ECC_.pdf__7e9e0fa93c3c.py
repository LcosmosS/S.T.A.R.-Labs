**Observation**:
- Errors skewed near symbolic degeneracy thresholds (`Smooth` ~ `Featured`).
- Entropy plateaus revealed projection drift zones with unstable symbolic attractors.
**Interpretation**:
- Errors reflect symbolic indeterminacy—not data noise.
- Inspired later symbolic reinitialization strategies via entropy field bootstrapping.
-----------------------------------------
VII. CONCLUSION
This extended appendix illustrates how ECC’s symbolic projection and curvature logic were
instantiated in real code, tested through entropy-aligned models, and validated using diagnostic
outputs. These early scripts not only predicted symbolic outcomes but provided structural insight
into entropy field evolution, curvature stability, and attractor formation. These foundational pieces
remain essential to understanding later model architectures in D.2–D.5.
Appendix D.2: Evolution of Symbolic Models — From Random Forests to
Gradient-Boosted Entropy Predictors
Appendix D.2 documents the critical methodological leap in ECC’s computational history: the
migration from entropy-enriched Random Forest regression to curvature-sensitive Gradient
Boosting ensembles. This progression was not merely algorithmic but fundamentally symbolic—the
movement from general-purpose learners to models capable of internally representing entropy
stratification, symbolic curvature, and projection identity dynamics. It reflects the transition of ECC
logic into computational ma...
-----------------------------------------
I. CONTEXTUAL FOUNDATIONS: WHY GRADIENT BOOSTING?
Random Forests served as an initial symbolic probe—a test for projection-based entropy sensitivity.However, the structure of ECC required:
- Continuous curvature flow approximation;
- Layer-wise symbolic decomposition of projection space;
- Entropy residual minimization across bifurcated identity strata.
Gradient Boosting emerged as a natural curvature-reflective framework due to:
- Stagewise additive modeling;
- Differentiable loss correction over symbolic manifolds;
- Integration with SHAP diagnostics for symbolic projection interpretability.
This set the stage for structured alignment between entropy fields and boosting logic.
-----------------------------------------
II. ALGORITHMIC SETUP AND ENTROPY-MATCHED REGRESSION
The entropy field target was `log_SFR_Ha`—not as a pure astrophysical proxy, but as a symbolic
entropy flux through projection space. Features included:
- `log_Mass_gas`, `log_Mass_stellar`: curvature anchors;
- `Av_gas_Re`, `OH_O3N2_cen`: symbolic energy attenuation;
- `Smooth`, `Featured`, `fM`, `pS`: morphological projection weights;
- `L_cosmo(s)`: entropy-mapped projection score;
- `BSD_likelihood`: symbolic identity projection filter.
The regression surface attempted to approximate a symbolic attractor manifold via entropy-aligned
decision trees.
```python
from sklearn.ensemble import GradientBoostingRegressor
gb_model = GradientBoostingRegressor(
n_estimators=300,
learning_rate=0.03,
max_depth=8,
subsample=0.85,
loss='ls'
)
gb_model.fit(X_train, y_train)
