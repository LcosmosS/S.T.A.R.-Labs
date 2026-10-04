    p_subtree_mutation=0.1,
    p_hoist_mutation=0.05,
    p_point_mutation=0.1,
    max_samples=0.9,
    verbose=1,
    parsimony_coefficient=0.0001,
    random_state=42,
    function_set=('add', 'sub', 'mul', 'div', 'sqrt', 'log', 'sin', 'cos'),
    n_jobs=2  # Use 2 CPU cores
)
symbolic_model.fit(X_train_selected_scaled, y_train)
y_pred_sym = symbolic_model.predict(X_test_selected_scaled)
r2_sym = r2_score(y_test, y_pred_sym)
print(f"gplearn R²: {r2_sym:.4f}")
print("Symbolic Expression:")
print(symbolic_model._program)

# Cross-validation for symbolic model
cv_scores_sym = cross_val_score(symbolic_model, X_train_selected_scaled, y_train, cv=5,
scoring='r2', n_jobs=2)
print(f"Symbolic Regression 5-Fold CV R²: Mean = {cv_scores_sym.mean():.4f}, Std =
