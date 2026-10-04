classifier = LogisticRegression(max_iter=Integer(1000), class_weight={Integer(1): Integer(50), Integer(0): Integer(1)}) --> 391 classifier.fit(np.array(X_data), np.array(y_data)) 392 


print(f"Classifier retrained. Coefficients: {classifier.coef_}") 394 max_successful_curves = Integer(30)


File /ext/sage/10.4/local/var/lib/sage/venv-python3.12.4/lib/python3.12/site-packages/sklearn/base.py:1473, in _fit_context.<locals>.decorator.<locals>.wrapper(estimator, *args, **kwargs) 1466 estimator._validate_params() 1468 with config_context( 1469 skip_parameter_validation=( 1470 prefer_skip_nested_validation or global_skip_validation 1471 ) 1472 ): -> 1473 return fit_method(estimator, *args, **kwargs) 


File /ext/sage/10.4/local/var/lib/sage/venv-python3.12.4/lib/python3.12/site-packages/sklearn/linear_model/_logistic.py:1223, in LogisticRegression.fit(self, X, y, sample_weight) 1220 else: 1221 _dtype = [np.float64, np.float32] -> 1223 X, y = self._validate_data( 1224 X, 1225 y, 1226 accept_sparse="csr", 1227 dtype=_dtype, 1228 order="C", 1229 accept_large_sparse=solver not in ["liblinear", "sag", "saga"], 1230 ) 1231 check_classification_targets(y) 1232 self.classes_ = np.unique(y) 


File /ext/sage/10.4/local/var/lib/sage/venv-python3.12.4/lib/python3.12/site-packages/sklearn/base.py:650, in BaseEstimator._validate_data(self, X, y, reset, validate_separately, cast_to_ndarray, **check_params) 648 y = check_array(y, input_name="y", **check_y_params) 649 else: --> 650 X, y = check_X_y(X, y, **check_params) 651 out = X, y 653 if not no_val_X and check_params.get("ensure_2d", True): 


File /ext/sage/10.4/local/var/lib/sage/venv-python3.12.4/lib/python3.12/site-packages/sklearn/utils/validation.py:1320, in check_X_y(X, y, accept_sparse, accept_large_sparse, dtype, order, copy, force_writeable, force_all_finite, ensure_2d, allow_nd, multi_output, ensure_min_samples, ensure_min_features, y_numeric, estimator) 1301 X = check_array( 1302 X, 1303 accept_sparse=accept_sparse, (...) 1315 input_name="X", 1316 ) 1318 y = _check_y(y, multi_output=multi_output, y_numeric=y_numeric, estimator=estimator) -> 1320 check_consistent_length(X, y) 1322 return X, y 
