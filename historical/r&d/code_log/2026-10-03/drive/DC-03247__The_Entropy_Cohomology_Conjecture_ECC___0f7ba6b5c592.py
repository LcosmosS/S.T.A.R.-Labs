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
