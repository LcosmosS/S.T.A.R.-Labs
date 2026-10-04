@interact
def f(n=(1..15), m=(1..15)):
    print("n * m = {} = {}".format(n * m, factor(n * m)))
    P = polygon([(0, 0), (0, n), (m, n), (m, 0)])
    P.show(aspect_ratio=1, gridlines='minor', figsize=[3, 3], xmax=14, ymax=14)