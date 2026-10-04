from scipy.stats import randint


rf_param_dist = {
    'n_estimators': randint(100, 500),   # Number of trees
    'max_features': ['sqrt', 'log2', None],  # Use sqrt or log2 for max_features
    'max_depth': randint(5, 50),  # Depth of trees
    'min_samples_split': randint(2, 20),  # Minimum samples for splitting a node
    'min_samples_leaf': randint(1, 20),  # Minimum samples at a leaf node
    'bootstrap': [True, False],  # Whether to use bootstrapping
}
