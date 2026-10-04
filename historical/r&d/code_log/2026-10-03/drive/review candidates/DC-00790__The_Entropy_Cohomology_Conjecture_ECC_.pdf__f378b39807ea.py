**Interpretation**:
- Regularization mapped entropy fold-smoothness into curvature modeling;
- SHAP showed reduced symbolic attractor noise and improved basin stability;
- Controlled bifurcation curvature led to cleaner symbolic projection manifolds.
**Results**:
- Test R²: 0.869
- Best performance in mid-entropy zones with curvature folds;
- Most resilient to symbolic overprojection drift near morphological plateaus.
-----------------------------------------
V. SYMBOLIC ATTRACTOR DYNAMICS COMPARISON
| Model | Test R² | SHAP Attractor Structure | Entropy Basin Stability | Morphology Coherence |
|-----------|---------|---------------------------|--------------------------|-----------------------|
| CatBoost | 0.857 | Layered and clean | Moderate | High |
| LightGBM | 0.864 | Coarse but sharp | Very High | Medium |
| XGBoost | 0.869 | Sharp and sparse | Very High | High |
**Conclusion**:
- All models enhanced symbolic curvature tracking;
- XGBoost produced the most topologically stable attractors;
- LightGBM provided the fastest symbolic entropy stabilization.
-----------------------------------------
VI. SYMBOLIC DIAGNOSTICS ACROSS MODELS
- SHAP summary overlays displayed consistent entropy feature hierarchies.
- `L_cosmo(s)`, `log_Mass_gas`, and `OH_O3N2_cen` consistently formed the symbolic attractor triad.
- Degeneracy points (where `Smooth ≈ Featured`) marked highest symbolic error densities.
Entropy-informed masking (via L_cosmo(s) stratification) produced local improvements of R² by up
to +6%.-----------------------------------------
VII. ECC STRUCTURAL ALIGNMENT
Each model was interpreted as a symbolic curvature processor:
- CatBoost: identity sheaf reconstructor for categorical zones;
- LightGBM: entropy manifold navigator via leaf-optimized curvature descent;
- XGBoost: symbolic topology stabilizer under entropy-matching regularization.
These roles allowed the ECC curvature manifold \( \omega = d(dℳ) \) to be embedded
computationally through symbolic projection logic.
-----------------------------------------
VIII. CONCLUSION
Appendix D.3 reveals that boosting models enriched with entropy-aligned architectural
logic—CatBoost, LightGBM, and XGBoost—not only improved numerical performance but advanced
the symbolic projection consistency central to the ECC framework. These models collectively
demonstrated that symbolic curvature could be encoded, learned, and preserved across
cohomological layers, making them indispensable to entropy-theoretic cosmological learning
systems.
Appendix D.4: Symbolic Model Expression via Genetic Programming and
Interpretable Structures
Appendix D.4 presents the formal development, deployment, and symbolic interpretation of
ECC-aligned regression models constructed via symbolic genetic programming. This effort was
driven by the need to extract **closed-form symbolic expressions** consistent with the Entropy
Cohomology Conjecture’s projection curvature, identity attractors, and entropy basin stratifications.
The approach centered around `gplearn`, a symbolic regression engine that mimics evolutionary
logic, enabling the derivation of...
-----------------------------------------
I. MOTIVATION FOR SYMBOLIC EXPRESSION DERIVATION
Standard boosting models offered entropy projection capabilities, but lacked:
- Explicit algebraic mappings of entropy to identity;
- Closed-form symbolic visibility into cohomology structure;
- Formal expressions to translate ECC curvature dynamics into analyzable equations.
Symbolic regression bridged ECC’s abstract topology to concrete formulae rooted in entropy logic.-----------------------------------------
II. TOOLING: GPlearn CONFIGURATION
GPlearn was selected due to:
- Support for user-defined function sets;
- Tree-based expression generation consistent with symbolic logic trees;
- Fitness metrics aligned with symbolic curvature error (e.g. RMSE and R²).
Example initialization:
```python
from gplearn.genetic import SymbolicRegressor
est_gp = SymbolicRegressor(population_size=2000,
generations=30,
stopping_criteria=0.001,
function_set=['add', 'sub', 'mul', 'div', 'log', 'sqrt'],
p_crossover=0.7,
p_subtree_mutation=0.1,
p_point_mutation=0.1,
metric='mean absolute error',
parsimony_coefficient=0.01,
random_state=42)
est_gp.fit(X_train, y_train)
