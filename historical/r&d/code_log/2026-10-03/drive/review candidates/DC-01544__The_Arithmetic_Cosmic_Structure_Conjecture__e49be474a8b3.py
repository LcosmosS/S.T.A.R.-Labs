from gplearn.genetic import SymbolicRegressor
from gplearn.functions import make_function
from gplearn.fitness import make_fitness


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             * Fitness Metric:


def entropy_adjusted_mse(y, y_pred, w):
      err = (y - y_pred)**2
      symbolic_penalty = np.var(w) * np.mean(np.abs(w - np.mean(w)))
      return np.mean(err) + 0.15 * symbolic_penalty


symbolic_fitness = make_fitness(entropy_adjusted_mse, greater_is_better=False)
