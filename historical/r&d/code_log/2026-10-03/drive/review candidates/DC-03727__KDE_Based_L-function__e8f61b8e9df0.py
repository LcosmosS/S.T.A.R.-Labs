from gplearn.functions import make_function
from numpy import log1p, tanh


function_set = ['add', 'sub', 'mul', 'div',
                make_function(function=log1p, name='log1p', arity=1),
                make_function(function=tanh, name='tanh', arity=1)]


symbolic_model = SymbolicRegressor(
    function_set=function_set,
    ...
)
