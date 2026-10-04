var('x')
@interact
def g(f='x*sin(1/x)',
      c=slider(-1, 1, .01, default=-.5),
      n=(1..30),
      xinterval=range_slider(-1, 1, .1, default=(-8,8), label="x-interval"),
      yinterval=range_slider(-1, 1, .1, default=(-3,3), label="y-interval")):
    f = eval(f)
    x0 = c
    degree = n
    xmin,xmax = xinterval
    ymin,ymax = yinterval
    p   = plot(f, xmin, xmax, thickness=4)
    dot = point((x0,f(x=x0)),pointsize=80,rgbcolor=(1,0,0))
    ft = f.taylor(x,x0,degree)
    pt = plot(ft, xmin, xmax, color='red', thickness=2, fill=f)
    show(dot + p + pt, ymin=ymin, ymax=ymax, xmin=xmin, xmax=xmax)
    html(r'$f(x)\;=\;%s$' % latex(f))
    html(r'$P_{%s}(x)\;=\;%s+R_{%s}(x)$' % (degree,latex(ft),degree))