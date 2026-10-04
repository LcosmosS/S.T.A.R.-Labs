%display latex
var('x,y')
f = (cos(pi/4 - x) - tan(x)) / (1 - sin(pi/4 + x))
limit(f, x = pi/4, dir='minus')