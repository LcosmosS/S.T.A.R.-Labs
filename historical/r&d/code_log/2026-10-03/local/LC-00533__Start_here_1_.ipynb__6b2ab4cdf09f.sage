L = RootSystem(["G", 2, 1]).ambient_space()
p = L.plot(affine=False, level=1)
p.show(aspect_ratio=[1, 1, 2], frame=False)