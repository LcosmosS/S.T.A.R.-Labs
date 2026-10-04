@interact
def plt(n=5, f=[sin, cos, tan]):
    return plot(f(n*x))